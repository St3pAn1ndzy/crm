from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


def upload_contract_document(instance, filename):
    return f"contracts/contract_{instance.customer.pk}/{filename}"


class Contract(models.Model):
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.CASCADE,
        verbose_name="Клиент",
    )
    title = models.CharField(max_length=150, verbose_name="Название контракта")

    service = models.ForeignKey(
        "services.Service",
        on_delete=models.PROTECT,
        verbose_name="Предоставляемая услуга",
    )

    document = models.FileField(
        upload_to=upload_contract_document,
        verbose_name="Файл с документом",
        help_text="Загрузите подписанный скан договора (PDF, DOCX)",
    )

    start_date = models.DateField(verbose_name="Дата заключения")

    end_date = models.DateField(verbose_name="Дата окончания действия")

    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Сумма",
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено в CRM")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено в CRM")

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Если снять галочку, контракт уйдет в архив",
    )

    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"
        ordering = ["-start_date"]

    def __str__(self):
        return f"Договор: {self.title} (от {self.start_date})"
