using System.Text.Json.Serialization;

namespace TelegramNotifierService.Services.Telegram.Entities;

public class SendMessageEntity
{
    public SendMessageEntity(long chatId, string text)
    {
        ChatId = chatId;
        Text = text;
    }
    
    [JsonPropertyName("chat_id")]
    public long ChatId { get; }
    
    [JsonPropertyName("text")]
    public string Text { get; }
}
