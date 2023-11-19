namespace TelegramNotifierService.Exceptions;

public class CategoryNotFoundException : LogicalException
{
    public CategoryNotFoundException() : base("Category not found")
    {
        
    }    
}
