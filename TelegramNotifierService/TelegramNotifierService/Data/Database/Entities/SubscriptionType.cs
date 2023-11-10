namespace TelegramNotifierService.Data.Database.Entities;

public partial class SubscriptionType
{
    public long Id { get; set; }

    public string Name { get; set; } = null!;

    public virtual ICollection<Subscription> Subscriptions { get; set; } = new List<Subscription>();
}
