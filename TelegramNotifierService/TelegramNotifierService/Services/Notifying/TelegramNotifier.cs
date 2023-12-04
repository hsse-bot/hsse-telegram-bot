using TelegramNotifierService.Services.Data;
using TelegramNotifierService.Services.Telegram;

namespace TelegramNotifierService.Services.Notifying;

public class TelegramNotifier : INotifier
{
    private readonly ITelegramBulkMessagingHelper _messagingHelper;
    private readonly ISubscriptionsManager _subscriptionsManager;

    public TelegramNotifier(ITelegramBulkMessagingHelper messagingHelper,
        ISubscriptionsManager subscriptionsManager)
    {
        _messagingHelper = messagingHelper;
        _subscriptionsManager = subscriptionsManager;
    }
    
    public async Task NotifyAllBySubscriptionAsync(long categoryId, string messageContent, CancellationToken cancellationToken)
    {
        var allByCategory = await _subscriptionsManager.GetAllSubscriptionsByCategoryAsync(categoryId);
        await _messagingHelper.SendBulkMessageAsync(allByCategory.Select(x => x.ConsumerId), messageContent, cancellationToken);
    }
}