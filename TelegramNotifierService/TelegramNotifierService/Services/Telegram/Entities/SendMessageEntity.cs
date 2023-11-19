namespace TelegramNotifierService.Services.Telegram.Entities;

public record SendMessageEntity(long ChatId, string Text);
