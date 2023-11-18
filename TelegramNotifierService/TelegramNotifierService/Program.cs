using Microsoft.EntityFrameworkCore;
using TelegramNotifierService;
using TelegramNotifierService.Data.Database;
using TelegramNotifierService.Data.Repositories;
using TelegramNotifierService.Services.Data;
using TelegramNotifierService.Services.Notifying;
using TelegramNotifierService.Services.Telegram;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddHttpClient("TelegramApiClient", client =>
{
    var token = EnvConfig.TgToken;
    client.BaseAddress = new Uri($"https://api.telegram.org/bot{token}");
});

var serverVersion = new MySqlServerVersion(new Version(8, 0, 34));

builder.Services.AddDbContext<TelegramNotifyingContext>(
    dbContextOptions =>
    {
        dbContextOptions.UseMySql(EnvConfig.DbConnectionString, serverVersion)
            .UseLazyLoadingProxies();
            
#if DEBUG
        dbContextOptions.LogTo(Console.WriteLine, LogLevel.Information)
            .EnableSensitiveDataLogging()
            .EnableDetailedErrors();
#endif
    });

builder.Services.AddScoped<ICategoriesRepository, CategoriesRepository>()
    .AddScoped<ISubscriptionsRepository, SubscriptionsRepository>()
    .AddScoped<ISubscriptionsManager, SubscriptionsManager>()
    .AddScoped<INotifier, TelegramNotifier>()
    .AddScoped<ITelegramBulkMessagingHelper, TelegramBulkMessagingHelper>();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();