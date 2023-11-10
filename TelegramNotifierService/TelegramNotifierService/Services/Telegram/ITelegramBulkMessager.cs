namespace TelegramNotifierService.Services.Telegram;

public interface ITelegramBulkMessager
{
    Task SendBulkMessageAsync(IEnumerable<long> consumersIds, string messageContent, CancellationToken cancellationToken);
}
