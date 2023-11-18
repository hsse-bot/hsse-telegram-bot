using Microsoft.EntityFrameworkCore;
using TelegramNotifierService.Data.Database.Entities;

namespace TelegramNotifierService.Data.Database;

public partial class TelegramNotifyingContext : DbContext
{
    public TelegramNotifyingContext()
    {
    }

    public TelegramNotifyingContext(DbContextOptions<TelegramNotifyingContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Subscription> Subscriptions { get; set; }

    public virtual DbSet<SubscriptionCategory> Categories { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder
            .UseCollation("utf8mb4_0900_ai_ci")
            .HasCharSet("utf8mb4");

        modelBuilder.Entity<Subscription>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PRIMARY");

            entity.ToTable("subscriptions");

            entity.HasIndex(e => e.CategoryId, "category_id");

            entity.Property(e => e.Id).HasColumnName("id");
            entity.Property(e => e.ConsumerId).HasColumnName("consumer_id");
            entity.Property(e => e.CategoryId).HasColumnName("category_id");

            entity.HasOne(d => d.Category).WithMany(p => p.Subscriptions)
                .HasForeignKey(d => d.CategoryId)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("subscriptions_ibfk_1");
        });

        modelBuilder.Entity<SubscriptionCategory>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PRIMARY");

            entity.ToTable("categories");

            entity.HasIndex(e => e.Name, "name").IsUnique();

            entity.Property(e => e.Id).HasColumnName("id");
            entity.Property(e => e.Name)
                .HasMaxLength(128)
                .HasColumnName("name")
                .UseCollation("utf8mb3_general_ci")
                .HasCharSet("utf8mb3");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
