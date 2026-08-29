from django.contrib import admin

from .models import Contract


@admin.action(description="Заархивировать выбранные контракты")
def make_archived(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(
        request, f"Успешно заархивировано объектов: {updated}."
    )


@admin.action(description="Разархивировать выбранные контракты")
def make_unarchived(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(
        request, f"Успешно разархивировано объектов: {updated}."
    )


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "customer", "service",
                    "start_date", "end_date", "cost", "is_active")
    list_filter = ("is_active", "start_date", "end_date", "service")
    search_fields = ("title", "customer__lead__last_name")
    list_editable = ("is_active",)
    date_hierarchy = "start_date"

    actions = [make_archived, make_unarchived]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions
