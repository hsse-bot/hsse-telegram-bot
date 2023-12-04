using System.Net;
using System.Text.Json;
using TelegramNotifierService.Services.Telegram.Entities;

namespace TelegramNotifierService.Services.Telegram;

public class TelegramBulkMessagingHelper : ITelegramBulkMessagingHelper
{
    private const int RequestsDelay = 100;
    private const string SendMessageApiMethodRoute = "sendMessage";
    
    private readonly HttpClient _tgClient;
    
    public TelegramBulkMessagingHelper(IHttpClientFactory clientFactory)
    {
        _tgClient = clientFactory.CreateClient("TelegramApiClient");
    }
    
    public Task SendBulkMessageAsync(IEnumerable<long> consumersIds,
        string messageContent,
        CancellationToken cancellationToken)
    {
        var consumersIdsArray = consumersIds as long[] ?? consumersIds.ToArray();
        var tasks = new Task[consumersIdsArray.Length];
        
        for (var i = 0; i < consumersIdsArray.Length; i++)
        {
            tasks[i] = SendMessage(consumersIdsArray[i], messageContent, cancellationToken);
        }

        Task.WaitAll(tasks, cancellationToken);

        return Task.CompletedTask;
    }

    private async Task SendMessage(long dest, string messageContent, CancellationToken cancellationToken)
    {
        using var memStream = new MemoryStream();
        var msg = new SendMessageEntity(dest, messageContent);
        
        var response = await _tgClient.PostAsJsonAsync(SendMessageApiMethodRoute, msg, cancellationToken);
        
        if (response.StatusCode == HttpStatusCode.TooManyRequests)
        {
            while (!response.IsSuccessStatusCode && !cancellationToken.IsCancellationRequested)
            {
                response = await _tgClient.PostAsJsonAsync(SendMessageApiMethodRoute, msg, cancellationToken: cancellationToken);
                await Task.Delay(RequestsDelay, cancellationToken);
            }
        }
    }
}