from django.contrib import admin

from .models import Service


@admin.action(description="Заархивировать выбранные услуги")
def make_archived(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(request, f"Успешно заархивировано объектов: {updated}.")


@admin.action(description="Разархивировать выбранные услуги")
def make_unarchived(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, f"Успешно разархивировано объектов: {updated}.")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("title", "description")
    list_editable = ("is_active", "price")

    actions = [make_archived, make_unarchived]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def delete_model(self, request, obj):
        obj.is_active = False
        obj.save(update_fields=["is_active"])

        self.message_user(
            request, f"Услуга'{obj.title}' была успешно отправлен в архив."
        )
