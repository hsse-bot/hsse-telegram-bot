using TelegramNotifierService.Services.Data;
using TelegramNotifierService.Services.Telegram;

namespace TelegramNotifierService.Services.Notifying;

public class TelegramNotifier : INotifier
{
    private readonly ITelegramBulkMessager _messager;
    private readonly ISubscriptionsManager _subscriptionsManager;

    public TelegramNotifier(ITelegramBulkMessager messager,
        ISubscriptionsManager subscriptionsManager)
    {
        _messager = messager;
        _subscriptionsManager = subscriptionsManager;
    }
    
    public async Task NotifyAllBySubscriptionAsync(long subTypeId, string messageContent, CancellationToken cancellationToken)
    {
        var allByCategory = await _subscriptionsManager.GetAllSubscriptionsByTypeAsync(subTypeId);
        await _messager.SendBulkMessageAsync(allByCategory.Select(x => x.Id), messageContent, cancellationToken);
    }
}