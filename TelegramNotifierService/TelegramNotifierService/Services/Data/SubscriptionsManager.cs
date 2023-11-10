using TelegramNotifierService.Data.Database.Entities;
using TelegramNotifierService.Data.Repositories;

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
    
    public async Task<SubscriptionType> CreateSubscriptionTypeAsync(string subscriptionName)
    {
        var subType = new SubscriptionType
        {
            Name = subscriptionName
        };
        
        await _subscriptionTypesRepository.AddAsync(subType);
        await _subscriptionTypesRepository.SaveChangesAsync();
        return subType;
    }

    public async Task DeleteSubscriptionTypeAsync(long subTypeId)
    {
        _subscriptionTypesRepository.Remove(new SubscriptionType
        {
            Id = subTypeId
        });

        await _subscriptionsRepository.SaveChangesAsync();
    }

    public Task<IEnumerable<Subscription>> GetAllSubscriptionsByConsumerAsync(long consumerId)
    {
        return Task.FromResult(_subscriptionsRepository.GetAll().Where(x => x.ConsumerId == consumerId));
    }

    public Task<IEnumerable<Subscription>> GetAllSubscriptionsByTypeAsync(long subTypeId)
    {
        return Task.FromResult(_subscriptionsRepository.GetAll().Where(x => x.TypeId == subTypeId));
    }

    public async Task<Subscription> SubscribeUserAsync(long consumerId, long subTypeId)
    {
        var sub = new Subscription
        {
            ConsumerId = consumerId,
            TypeId = subTypeId
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
            TypeId = subTypeId
        });

        await _subscriptionsRepository.SaveChangesAsync();
    }
}
