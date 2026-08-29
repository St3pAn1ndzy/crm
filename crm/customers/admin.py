from django.contrib import admin

from .models import Customer


@admin.action(description="Заархивировать выбранных клиентов")
def make_archived(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(
        request, f"Успешно заархивировано объектов: {updated}."
    )


@admin.action(description="Разархивировать выбранных клиентов")
def make_unarchived(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(
        request, f"Успешно разархивировано объектов: {updated}."
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "get_client_name", "get_client_phone",
                    "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("lead__first_name",
                     "lead__last_name", "lead__phone")
    list_editable = ("is_active",)

    actions = [make_archived, make_unarchived]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    @admin.display(description="ФИО Клиента")
    def get_client_name(self, obj):
        return f"{obj.lead.first_name} {obj.lead.last_name}"

    @admin.display(description="Телефон")
    def get_client_phone(self, obj):
        return obj.lead.phone
