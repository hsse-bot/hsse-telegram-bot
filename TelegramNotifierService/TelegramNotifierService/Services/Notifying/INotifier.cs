namespace TelegramNotifierService.Services.Notifying;

public interface INotifier
{
    Task NotifyAllBySubscriptionAsync(long categoryId, string messageContent, CancellationToken cancellationToken);
}