namespace TelegramNotifierService.Services.Notifying;

public interface INotifier
{
    Task NotifyAllBySubscriptionAsync(long subTypeId, string messageContent, CancellationToken cancellationToken);
}