using TelegramNotifierService.Data.Database.Entities;
using TelegramNotifierService.Data.Repositories;
using TelegramNotifierService.Exceptions;

namespace TelegramNotifierService.Services.Data;

public class SubscriptionsManager : ISubscriptionsManager
{
    private readonly ISubscriptionsRepository _subscriptionsRepository;
    private readonly ISubscriptionTypesRepository _subscriptionTypesRepository;

    public SubscriptionsManager(ISubscriptionsRepository subscriptionsRepository,
        ISubscriptionTypesRepository subscriptionTypesRepository)
    {
        _subscriptionsRepository = subscriptionsRepository;
        _subscriptionTypesRepository = subscriptionTypesRepository;
    }
    
    public async Task<SubscriptionCategory> CreateSubscriptionTypeAsync(string subscriptionName)
    {
        var subType = new SubscriptionCategory
        {
            Name = subscriptionName
        };
        
        await _subscriptionTypesRepository.AddAsync(subType);
        await _subscriptionTypesRepository.SaveChangesAsync();
        return subType;
    }

    public async Task DeleteSubscriptionTypeAsync(long subTypeId)
    {
        _subscriptionTypesRepository.Remove(new SubscriptionCategory
        {
            Id = subTypeId
        });

        await _subscriptionsRepository.SaveChangesAsync();
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
        var type = await _subscriptionTypesRepository.FindAsync(subTypeId);

        if (type == null)
        {
            throw new CategoryNotFoundException();
        }

        return type;
    }
}
