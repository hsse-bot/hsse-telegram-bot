using TelegramNotifierService.Data.Api.Responses;
using TelegramNotifierService.Exceptions;

namespace TelegramNotifierService.Middlewares;

public class ExceptionsHandlingMiddleware
{
    private const int BadRequestStatusCode = 400;
    private const int InternalServerErrorStatusCode = 500;
    
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionsHandlingMiddleware> _logger;

    public ExceptionsHandlingMiddleware(RequestDelegate next, 
        ILogger<ExceptionsHandlingMiddleware> logger)
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
        catch (Exception e)
        {
            context.Response.StatusCode = InternalServerErrorStatusCode;
            await context.Response.WriteAsJsonAsync(ErrorResponse.FromException(e));
            _logger.LogError(e, "Exception");

#if DEBUG
            throw;
#endif
        }
    }
}