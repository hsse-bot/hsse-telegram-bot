using TelegramNotifierService.Data.Database.Entities;

namespace TelegramNotifierService.Data.Repositories;

public interface ISubscriptionTypesRepository
{
    /// <summary>
    /// Получает все типы подписок
    /// </summary>
    IEnumerable<SubscriptionType> GetAll();
    
    /// <summary>
    /// Находит тип подписки
    /// </summary>
    /// <param name="id">ID типа подписки</param>
    /// <returns>Null, если тип подписки не найден, иначе значение</returns>
    Task<SubscriptionType?> FindAsync(long id);
    
    /// <summary>
    /// Добавляет тип подписки
    /// </summary>
    /// <param name="subscription">Объект подписки</param>
    Task AddAsync(SubscriptionType subscription);
    
    /// <summary>
    /// Удаляет тип подписки
    /// </summary>
    /// <param name="subscription">Тип подписки, которую нужно удалить</param>
    void Remove(SubscriptionType subscription);
    
    /// <summary>
    /// Сохраняет изменения
    /// </summary>
    Task SaveChangesAsync();
}
