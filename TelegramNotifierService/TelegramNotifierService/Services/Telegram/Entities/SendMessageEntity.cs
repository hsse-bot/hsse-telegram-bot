namespace TelegramNotifierService.Services.Telegram.Entities;

public record SendMessageEntity(long chatId, string text);
