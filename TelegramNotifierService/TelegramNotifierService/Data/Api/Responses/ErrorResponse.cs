using System.Text.Json.Serialization;
using TelegramNotifierService.Exceptions;

namespace TelegramNotifierService.Data.Api.Responses;

public class ErrorResponse
{
    private const string UnknownErrorTag = "UNKNOWN_ERROR";
    
    public ErrorResponse(string tag, string message)
    {
        Tag = tag;
        Message = message;
    }
    
    [JsonPropertyName("tag")]
    public string Tag { get; }
    
    [JsonPropertyName("message")]
    public string Message { get; }
    
    public static ErrorResponse FromException(Exception exception)
    {
        if (exception is LogicalException logicalException)
        {
            return new ErrorResponse(logicalException.Tag, logicalException.Message);
        }

        return new ErrorResponse(UnknownErrorTag, exception.Message);
    }
}