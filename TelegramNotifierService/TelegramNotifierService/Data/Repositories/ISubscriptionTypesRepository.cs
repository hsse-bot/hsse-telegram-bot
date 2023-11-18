using TelegramNotifierService.Data.Database.Entities;

namespace TelegramNotifierService.Data.Repositories;

public interface ISubscriptionTypesRepository
{
    /// <summary>
    /// Получает все типы подписок
    /// </summary>
    IEnumerable<SubscriptionCategory> GetAll();
    
    /// <summary>
    /// Находит тип подписки
    /// </summary>
    /// <param name="id">ID типа подписки</param>
    /// <returns>Null, если тип подписки не найден, иначе значение</returns>
    Task<SubscriptionCategory?> FindAsync(long id);
    
    /// <summary>
    /// Добавляет тип подписки
    /// </summary>
    /// <param name="subscription">Объект подписки</param>
    Task AddAsync(SubscriptionCategory subscription);
    
    /// <summary>
    /// Удаляет тип подписки
    /// </summary>
    /// <param name="subscription">Тип подписки, которую нужно удалить</param>
    void Remove(SubscriptionCategory subscription);
    
    /// <summary>
    /// Сохраняет изменения
    /// </summary>
    Task SaveChangesAsync();
}
