from django.db import models


class Ad(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название кампании"
    )
    channel = models.CharField(
        max_length=100,
        verbose_name="Канал продвижения",
        help_text="Например: Яндекс.Директ, Telegram, VK"
    )
    product = models.ForeignKey(
        "services.Service",
        on_delete=models.PROTECT,
        verbose_name="Продвигаемая услуга"
    )
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Бюджет"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
        help_text="Если снять галочку, продвижение прекратиться"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Рекламная кампания"
        verbose_name_plural = "Рекламные кампании"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.title} ({self.channel})"
