from django.contrib import admin

from .models import Customer


@admin.action(description="Заархивировать выбранных клиентов")
def make_archived(modeladmin, request, queryset):
    for obj in queryset:
        if hasattr(obj, 'contract_set'):
            obj.contract_set.filter(is_active=True).update(is_active=False)

        if obj.lead:
            obj.lead.status = "refused"
            obj.lead.save(update_fields=["status"])

    updated = queryset.update(is_active=False)
    modeladmin.message_user(
        request, f"Успешно заархивировано клиентов: {updated} "
                 f"(связанные лиды переведены в статус 'Отказ')."
    )


@admin.action(description="Разархивировать выбранных клиентов")
def make_unarchived(modeladmin, request, queryset):
    for obj in queryset:
        if hasattr(obj, 'contract_set'):
            obj.contract_set.filter(is_active=False).update(is_active=True)

        if obj.lead:
            obj.lead.status = "converted"
            obj.lead.save(update_fields=["status"])

    updated = queryset.update(is_active=True)
    modeladmin.message_user(
        request,
        f"Успешно восстановлено клиентов из архива: {updated} "
        f"(связанные контракты активированы, статус лидов изменен на 'Сконвертирован')."
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

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("lead")

    def delete_view(self, request, object_id, extra_context=None):

        if request.POST:
            obj = self.get_object(request, object_id)
            if obj:
                if hasattr(obj, 'contract_set'):
                    obj.contract_set.filter(is_active=True).update(is_active=False)

                if obj.lead:
                    obj.lead.status = "refused"
                    obj.lead.save(update_fields=["status"])

                obj.is_active = False
                obj.save(update_fields=["is_active"])

                client_name = f"{obj.lead.first_name} {obj.lead.last_name}" \
                    if obj.lead else f"ID {obj.id}"
                self.message_user(request, f"Клиент '{client_name}' и его "
                                           f"контракты успешно заархивированы.")

                from django.http import HttpResponseRedirect
                return HttpResponseRedirect(request.path.split('/delete/')[0] + '/')

        return super().delete_view(request, object_id, extra_context=extra_context)
