namespace TelegramNotifierService.Data.Database.Entities;

public partial class Subscription
{
    public long Id { get; set; }

    public long ConsumerId { get; set; }

    public long TypeId { get; set; }

    public virtual SubscriptionType Type { get; set; } = null!;
}
