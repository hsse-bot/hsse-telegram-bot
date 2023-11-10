using TelegramNotifierService.Data.Database.Entities;

namespace TelegramNotifierService.Data.Repositories;

public interface ISubscriptionsRepository
{
    /// <summary>
    /// Получает все подписки
    /// </summary>
    IEnumerable<Subscription> GetAll();
    
    /// <summary>
    /// Находит подпсику
    /// </summary>
    /// <param name="id">ID подписки</param>
    /// <returns>Null, если подписка не найдена, иначе значение</returns>
    Task<Subscription?> FindAsync(long id);
    
    /// <summary>
    /// Добавляет подписку
    /// </summary>
    /// <param name="subscription">Объект подписки</param>
    Task AddAsync(Subscription subscription);
    
    /// <summary>
    /// Удаляет подписку
    /// </summary>
    /// <param name="subscription">Подписку, которую нужно удалить</param>
    void Remove(Subscription subscription);
    
    /// <summary>
    /// Сохраняет изменения
    /// </summary>
    Task SaveChangesAsync();
}