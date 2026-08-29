from django.contrib import admin

from .models import Lead


@admin.action(description="Заархивировать выбранных лидов")
def make_archived(modeladmin, request, queryset):
    updated = queryset.update(status="refused")
    modeladmin.message_user(request, f"Успешно заархивировано объектов: {updated}.")


@admin.action(description="Разархивировать выбранных лидов")
def make_unarchived(modeladmin, request, queryset):
    updated = queryset.update(status="new")
    modeladmin.message_user(request, f"Успешно разархивировано объектов: {updated}.")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone",
        "email",
        "advertisement",
        "status",
    )
    list_filter = ("status", "advertisement")
    search_fields = ("first_name", "last_name", "phone", "email")
    list_editable = ("status",)

    actions = [make_archived, make_unarchived]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def delete_model(self, request, obj):
        obj.status = "refused"
        obj.save(update_fields=["status"])

        self.message_user(
            request,
            f"Лид '{obj.first_name} {obj.last_name}' была успешно отправлен в архив.",
        )
