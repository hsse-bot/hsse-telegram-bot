namespace TelegramNotifierService;

public static class EnvConfig
{
   public static string DbConnectionString => GetEnvVar("MY_SQL_CONNECTION_STRING");
   public static string TgToken => GetEnvVar("TG_TOKEN");
   
   private static string GetEnvVar(string name)
   {
      var value = Environment.GetEnvironmentVariable(name);

      if (value == null)
      {
         throw new InvalidOperationException($"The \"{name}\" env variable is null");
      }

      return value;
   }
}