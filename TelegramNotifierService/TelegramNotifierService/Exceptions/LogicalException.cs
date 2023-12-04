namespace TelegramNotifierService.Exceptions;

public class LogicalException : Exception
{
    public LogicalException(string tag)
    {
        Tag = tag;
    }

    public LogicalException(string tag, string message) : base(message)
    {
        Tag = tag;
    }
    
    public string Tag { get; }
}
