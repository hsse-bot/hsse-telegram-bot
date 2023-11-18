using TelegramNotifierService.Data.Database.Entities;

namespace TelegramNotifierService.Services.Data;

public interface ISubscriptionsManager
{
    Task<SubscriptionCategory> CreateSubscriptionTypeAsync(string subscriptionName);
    Task DeleteSubscriptionTypeAsync(long subTypeId);
    Task<IEnumerable<Subscription>> GetAllSubscriptionsByConsumerAsync(long consumerId);
    Task<IEnumerable<Subscription>> GetAllSubscriptionsByCategoryAsync(long subTypeId);
    Task<Subscription> SubscribeUserAsync(long consumerId, long subTypeId);
    Task UnsubscribeUserAsync(long consumerId, long subTypeId);
}