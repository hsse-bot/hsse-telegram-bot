using TelegramNotifierService.Data.Database.Entities;

namespace TelegramNotifierService.Services.Data;

public interface ISubscriptionsManager
{
    Task<SubscriptionCategory> CreateCategoryAsync(string subscriptionName);
    Task<SubscriptionCategory> GetCategoryAsync(long id);
    Task<IEnumerable<SubscriptionCategory>> GetCategoriesAsync();
    Task DeleteCategoryAsync(long id);
    Task DeleteSubscriptionTypeAsync(long subTypeId);
    Task<IEnumerable<Subscription>> GetAllSubscriptionsByConsumerAsync(long consumerId);
    Task<IEnumerable<Subscription>> GetAllSubscriptionsByCategoryAsync(long subTypeId);
    Task<Subscription> SubscribeUserAsync(long consumerId, long subTypeId);
    Task UnsubscribeUserAsync(long consumerId, long subTypeId);
}