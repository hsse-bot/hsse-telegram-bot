namespace TelegramNotifierService.Exceptions;

public class CategoryNotFoundException : LogicalException
{
    private const string ExceptionTag = "SUBSCRIPTION_NOT_FOUND";
    
    public CategoryNotFoundException() : base(ExceptionTag, "Category not found")
    {
        
    }    
}
