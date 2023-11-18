namespace TelegramNotifierService.Data.Database.Entities;

public partial class Subscription
{
    public long Id { get; set; }

    public long ConsumerId { get; set; }

    public long CategoryId { get; set; }

    public virtual SubscriptionCategory Category { get; set; } = null!;
}
