namespace TelegramNotifierService.Services.Telegram;

public interface ITelegramBulkMessagingHelper
{
    Task SendBulkMessageAsync(IEnumerable<long> consumersIds, string messageContent, CancellationToken cancellationToken);
}
