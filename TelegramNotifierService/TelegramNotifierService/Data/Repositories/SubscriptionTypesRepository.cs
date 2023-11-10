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

    public IEnumerable<SubscriptionType> GetAll() => 
        _dbContext.SubscriptionTypes;

    public Task<SubscriptionType?> FindAsync(long id) =>
        _dbContext.SubscriptionTypes.FindAsync(id).AsTask();

    public async Task AddAsync(SubscriptionType subscription)
    {
        await _dbContext.AddAsync(subscription);
    }

    public void Remove(SubscriptionType subscription) => 
        _dbContext.SubscriptionTypes.Remove(subscription);

    public async Task SaveChangesAsync()
    {
        await _dbContext.SaveChangesAsync();
    }
}
