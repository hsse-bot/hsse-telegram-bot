FROM mcr.microsoft.com/dotnet/aspnet:7.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
WORKDIR /src
COPY ["./TelegramNotifierService.csproj", "TelegramNotifierService/"]
RUN dotnet restore "TelegramNotifierService/TelegramNotifierService.csproj"
WORKDIR "/src/TelegramNotifierService"
COPY . .
RUN dotnet build "TelegramNotifierService.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "TelegramNotifierService.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "TelegramNotifierService.dll"]
