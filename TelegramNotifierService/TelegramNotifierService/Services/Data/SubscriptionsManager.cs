using TelegramNotifierService.Data.Database.Entities;
using TelegramNotifierService.Data.Repositories;
using TelegramNotifierService.Exceptions;

namespace TelegramNotifierService.Services.Data;

public class SubscriptionsManager : ISubscriptionsManager
{
    private readonly ISubscriptionsRepository _subscriptionsRepository;
    private readonly ICategoriesRepository _categoriesRepository;

    public SubscriptionsManager(ISubscriptionsRepository subscriptionsRepository,
        ICategoriesRepository categoriesRepository)
    {
        _subscriptionsRepository = subscriptionsRepository;
        _categoriesRepository = categoriesRepository;
    }
    
    public async Task<SubscriptionCategory> CreateCategoryAsync(string subscriptionName)
    {
        var subType = new SubscriptionCategory
        {
            Name = subscriptionName
        };
        
        await _categoriesRepository.AddAsync(subType);
        await _categoriesRepository.SaveChangesAsync();
        return subType;
    }
    
    public async Task<SubscriptionCategory> GetCategoryAsync(long id)
    {
        var result = await _categoriesRepository.FindAsync(id);

        if (result == null)
        {
            throw new CategoryNotFoundException();
        }

        return result;
    }
    
    public Task<IEnumerable<SubscriptionCategory>> GetCategoriesAsync()
    {
        return Task.FromResult(_categoriesRepository.GetAll());
    }

    public async Task DeleteCategoryAsync(long id)
    {
        try
        {
            _categoriesRepository.Remove(new SubscriptionCategory()
            {
                Id = id
            });

            await _categoriesRepository.SaveChangesAsync();
        }
        catch (Exception)
        {
            throw new CategoryNotFoundException();
        }
    }

    public Task<IEnumerable<Subscription>> GetAllSubscriptionsByConsumerAsync(long consumerId)
    {
        return Task.FromResult(_subscriptionsRepository.GetAll().Where(x => x.ConsumerId == consumerId));
    }

    public async Task<IEnumerable<Subscription>> GetAllSubscriptionsByCategoryAsync(long subTypeId)
    {
        var type = await FindSubTypeAsync(subTypeId);

        return type.Subscriptions;
    }

    public async Task<Subscription> SubscribeUserAsync(long consumerId, long subTypeId)
    {
        var sub = new Subscription
        {
            ConsumerId = consumerId,
            CategoryId = subTypeId
        };

        await _subscriptionsRepository.AddAsync(sub);
        await _subscriptionsRepository.SaveChangesAsync();
        return sub;
    }

    public async Task UnsubscribeUserAsync(long consumerId, long subTypeId)
    {
        _subscriptionsRepository.Remove(new Subscription
        {
            ConsumerId = consumerId,
            CategoryId = subTypeId
        });

        await _subscriptionsRepository.SaveChangesAsync();
    }

    private async Task<SubscriptionCategory> FindSubTypeAsync(long subTypeId)
    {
        var type = await _categoriesRepository.FindAsync(subTypeId);

        if (type == null)
        {
            throw new CategoryNotFoundException();
        }

        return type;
    }
}
