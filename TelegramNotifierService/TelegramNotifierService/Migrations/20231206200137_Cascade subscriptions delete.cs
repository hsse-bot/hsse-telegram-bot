using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace TelegramNotifierService.Migrations
{
    /// <inheritdoc />
    public partial class Cascadesubscriptionsdelete : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "subscriptions_ibfk_1",
                table: "subscriptions");

            migrationBuilder.AddForeignKey(
                name: "subscriptions_ibfk_1",
                table: "subscriptions",
                column: "category_id",
                principalTable: "categories",
                principalColumn: "id",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "subscriptions_ibfk_1",
                table: "subscriptions");

            migrationBuilder.AddForeignKey(
                name: "subscriptions_ibfk_1",
                table: "subscriptions",
                column: "category_id",
                principalTable: "categories",
                principalColumn: "id");
        }
    }
}
