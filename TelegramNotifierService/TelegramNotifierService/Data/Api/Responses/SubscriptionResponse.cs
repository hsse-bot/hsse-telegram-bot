using TelegramNotifierService.Data.Database.Entities;

namespace TelegramNotifierService.Data.Api.Responses;

public class SubscriptionResponse
{
    public SubscriptionResponse(long consumerId, long categoryId)
    {
        ConsumerId = consumerId;
        CategoryId = categoryId;
    }

    public long ConsumerId { get; }
    public long CategoryId { get; }

    public static SubscriptionResponse FromDb(Subscription subscription) =>
        new(subscription.ConsumerId, subscription.CategoryId);
}