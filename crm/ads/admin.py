from django.contrib import admin

from .models import Ad


@admin.action(description="Заархивировать выбранные рекламные кампании")
def make_archived(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(
        request, f"Успешно заархивировано объектов: {updated}."
    )


@admin.action(description="Разархивировать выбранные рекламные кампании")
def make_unarchived(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(
        request, f"Успешно разархивировано объектов: {updated}."
    )


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "channel", "product", "budget", "is_active")
    list_filter = ("channel", "is_active", "product")
    search_fields = ("title", "channel")
    list_editable = ("is_active",)

    actions = [make_archived, make_unarchived]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions
