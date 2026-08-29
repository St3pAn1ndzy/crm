from django.db import models


class Customer(models.Model):
    lead = models.OneToOneField(
        "leads.Lead",
        on_delete=models.PROTECT,
        verbose_name="Потенциальный клиент (лид)",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Если снять галочку, клиент уйдет в архив CRM",
    )

    class Meta:
        verbose_name = "Активный клиент"
        verbose_name_plural = "Активные клиенты"

    def __str__(self):
        return f"Клиент: {self.lead.first_name} {self.lead.last_name}"
