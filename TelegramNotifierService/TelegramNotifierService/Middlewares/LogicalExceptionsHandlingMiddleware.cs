using TelegramNotifierService.Data.Api.Responses;
using TelegramNotifierService.Exceptions;

namespace TelegramNotifierService.Middlewares;

public class LogicalExceptionsHandlingMiddleware
{
    private const int BadRequestStatusCode = 401;
    
    private readonly RequestDelegate _next;
    private readonly ILogger<LogicalExceptionsHandlingMiddleware> _logger;

    public LogicalExceptionsHandlingMiddleware(RequestDelegate next,
        ILogger<LogicalExceptionsHandlingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (LogicalException e)
        {
            context.Response.StatusCode = BadRequestStatusCode;
            await context.Response.WriteAsJsonAsync(ErrorResponse.FromException(e));
        }
    }
}