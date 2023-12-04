namespace TelegramNotifierService.Exceptions;

public class SubscriptionNotFoundException : LogicalException
{
    private const string ExceptionTag = "SUBSCRIPTION_NOT_FOUND";
    
    public SubscriptionNotFoundException() : base(ExceptionTag, "Subscription not found")
    {
    }
}