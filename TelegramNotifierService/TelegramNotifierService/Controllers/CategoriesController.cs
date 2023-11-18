using Microsoft.AspNetCore.Mvc;
using TelegramNotifierService.Data.Api.Requests;
using TelegramNotifierService.Data.Api.Responses;
using TelegramNotifierService.Services.Data;

namespace TelegramNotifierService.Controllers;

[Route("categories")]
[Produces("application/json")]
[ApiController]
public class CategoriesController : ControllerBase
{
    private readonly ISubscriptionsManager _subscriptionsManager;

    public CategoriesController(ISubscriptionsManager subscriptionsManager)
    {
        _subscriptionsManager = subscriptionsManager;
    }

    [HttpGet]
    public async Task<IActionResult> GetCategories()
    {
        var allCategories = await _subscriptionsManager.GetCategoriesAsync();

        return Ok(allCategories.Select(CategoryResponse.FromDb));
    }
    
    [HttpGet("{id:long}")]
    public async Task<IActionResult> GetCategory([FromRoute] long id)
    {
        var category = await _subscriptionsManager.GetCategoryAsync(id);

        return Ok(CategoryResponse.FromDb(category));
    }

    [HttpPost]
    public async Task<IActionResult> CreateCategory([FromBody] CreateCategoryRequest request)
    {
        var category = await _subscriptionsManager.CreateCategoryAsync(request.Name);

        return Ok(CategoryResponse.FromDb(category));
    }

    [HttpDelete("{id:long}")]
    public async Task<IActionResult> DeleteCategory([FromRoute] long id)
    {
        await _subscriptionsManager.DeleteCategoryAsync(id);

        return Ok();
    }
}
