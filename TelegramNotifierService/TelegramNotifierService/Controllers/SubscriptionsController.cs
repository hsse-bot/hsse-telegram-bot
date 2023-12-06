using Microsoft.AspNetCore.Mvc;
using TelegramNotifierService.Data.Api.Responses;
using TelegramNotifierService.Services.Data;

namespace TelegramNotifierService.Controllers;

[Route("subscriptions")]
[ApiController]
[Produces("application/json")]
public class SubscriptionsController : ControllerBase
{
    private readonly ISubscriptionsManager _subscriptionsManager;

    public SubscriptionsController(ISubscriptionsManager subscriptionsManager)
    {
        _subscriptionsManager = subscriptionsManager;
    }

    [HttpGet("{consumerId:long}/categories")]
    public async Task<IActionResult> GetCategories([FromRoute] long consumerId)
    {
        var subs = await _subscriptionsManager.GetAllSubscriptionsByConsumerAsync(consumerId);

        return Ok(subs.ToList().Select(x => CategoryResponse.FromDb(x.Category)));
    }
    
    [HttpPost("{consumerId:long}/categories/{categoryId:long}/subscribe")]
    public async Task<IActionResult> Subscribe(
        [FromRoute] long consumerId,
        [FromRoute] long categoryId)
    {
        var sub = await _subscriptionsManager.SubscribeUserAsync(consumerId, categoryId);

        return Ok(SubscriptionResponse.FromDb(sub));
    }
    
    [HttpDelete("{consumerId:long}/categories/{categoryId:long}/unsubscribe")]
    public async Task<IActionResult> Unsubscribe(
        [FromRoute] long consumerId,
        [FromRoute] long categoryId)
    {
        await _subscriptionsManager.UnsubscribeUserAsync(consumerId, categoryId);

        return Ok();
    }
}
