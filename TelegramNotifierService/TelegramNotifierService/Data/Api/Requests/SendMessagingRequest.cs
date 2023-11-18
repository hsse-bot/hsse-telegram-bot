using System.Text.Json.Serialization;

namespace TelegramNotifierService.Data.Api.Requests;

public class SendMessagingRequest
{
    [JsonConstructor]
    public SendMessagingRequest(string text, long categoryId)
    {
        Text = text;
        CategoryId = categoryId;
    }
    
    public string Text { get; }
    public long CategoryId { get; }
}
