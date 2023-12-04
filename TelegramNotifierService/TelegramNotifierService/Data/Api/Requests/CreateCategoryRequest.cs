using System.Text.Json.Serialization;

namespace TelegramNotifierService.Data.Api.Requests;

public class CreateCategoryRequest
{
   [JsonConstructor]
   public CreateCategoryRequest(string name)
   {
      Name = name;
   }

   public string Name { get; } 
}