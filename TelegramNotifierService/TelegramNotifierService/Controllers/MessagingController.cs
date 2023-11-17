using Microsoft.AspNetCore.Mvc;
using TelegramNotifierService.Data.Api.Requests;
using TelegramNotifierService.Services.Notifying;

namespace TelegramNotifierService.Controllers;

[Route("messaging")]
[Produces("application/json")]
[ApiController]
public class MessagingController : ControllerBase
{
    private readonly INotifier _notifier;

    public MessagingController(INotifier notifier)
    {
        _notifier = notifier;
    }

    [HttpPost("send")]
    public async Task<IActionResult> SendBulkMessaging(
        [FromBody] SendMessagingRequest request,
        CancellationToken cancellationToken)
    {
        await _notifier.NotifyAllBySubscriptionAsync(request.CategoryId, request.Text, cancellationToken);
        return Ok();
    }
}
