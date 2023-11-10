namespace TelegramNotifierService.Services.Telegram;

public interface ITelegramBulkMessager
{
    Task SendBulkMessage(IEnumerable<long> consumersIds, string messageContent, CancellationToken cancellationToken);
}
