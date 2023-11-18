using TelegramNotifierService.Data.Database.Entities;

namespace TelegramNotifierService.Data.Api.Responses;

public class CategoryResponse
{
    public CategoryResponse(long id, string name)
    {
        Id = id;
        Name = name;
    }

    public long Id { get; }
    public string Name { get; }

    public static CategoryResponse FromDb(SubscriptionCategory category) => new(category.Id, category.Name);
}
