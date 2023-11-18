using System.Text.Json.Serialization;

namespace TelegramNotifierService.Data.Api.Responses;

public class ErrorResponse
{
    public ErrorResponse(string message)
    {
        Message = message;
    }
    
    [JsonPropertyName("message")]
    public string Message { get; }

    public static ErrorResponse FromException(Exception exception) => new(exception.Message);
}