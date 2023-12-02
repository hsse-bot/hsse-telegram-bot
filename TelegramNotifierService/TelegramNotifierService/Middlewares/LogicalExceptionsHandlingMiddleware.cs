using TelegramNotifierService.Data.Api.Responses;
using TelegramNotifierService.Exceptions;

namespace TelegramNotifierService.Middlewares;

public class LogicalExceptionsHandlingMiddleware
{
    private const int BadRequestStatusCode = 400;
    
    private readonly RequestDelegate _next;

    public LogicalExceptionsHandlingMiddleware(RequestDelegate next)
    {
        _next = next;
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