using TelegramNotifierService.Data.Database;
using TelegramNotifierService.Data.Database.Entities;

namespace TelegramNotifierService.Data.Repositories;

public class SubscriptionTypesRepository : ISubscriptionTypesRepository
{
    private readonly TelegramNotifyingContext _dbContext;
    
    public SubscriptionTypesRepository(TelegramNotifyingContext dbContext)
    {
        _dbContext = dbContext;
    }

    public IEnumerable<SubscriptionCategory> GetAll() => 
        _dbContext.Categories;

    public Task<SubscriptionCategory?> FindAsync(long id) =>
        _dbContext.Categories.FindAsync(id).AsTask();

    public async Task AddAsync(SubscriptionCategory subscription)
    {
        await _dbContext.AddAsync(subscription);
    }

    public void Remove(SubscriptionCategory subscription) => 
        _dbContext.Categories.Remove(subscription);

    public async Task SaveChangesAsync()
    {
        await _dbContext.SaveChangesAsync();
    }
}
