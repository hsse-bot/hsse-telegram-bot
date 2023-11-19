using TelegramNotifierService.Data.Database;
using TelegramNotifierService.Data.Database.Entities;

namespace TelegramNotifierService.Data.Repositories;

public class SubscriptionsRepository : ISubscriptionsRepository
{
    private readonly TelegramNotifyingContext _dbContext;

    public SubscriptionsRepository(TelegramNotifyingContext dbContext)
    {
        _dbContext = dbContext;
    }

    public IEnumerable<Subscription> GetAll() => 
        _dbContext.Subscriptions;

    public Task<Subscription?> FindAsync(long id) => 
        _dbContext.Subscriptions.FindAsync(id).AsTask();

    public async Task AddAsync(Subscription subscription) => 
        await _dbContext.AddAsync(subscription);

    public void Remove(Subscription subscription) =>
        _dbContext.Remove(subscription);

    public async Task SaveChangesAsync() => 
        await _dbContext.SaveChangesAsync();
}
