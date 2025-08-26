from django.contrib import admin
from .models import NetworkNode, Supplier, NetworkObject
from django.urls import reverse
from django.utils.html import format_html


def reset_field(obj, field_name):
    # Пример очистки конкретного поля
    if hasattr(obj, field_name):
        setattr(obj, field_name, None)
        obj.save(update_fields=[field_name])


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'country', 'city', 'street', 'house_number', 'actions_link')
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'country', 'city', 'street', 'house_number')
        }),
    )

    # Кнопка очистки конкретного поля на странице редактирования объекта
    def actions_link(self, obj):
        # Здесь можно перечислить конкретные поля и соответствующие ссылки
        # Например, кнопка очистки email
        return format_html(
            '<a class="button" href="{}">Очистить Email</a>',
            reverse('admin:clear_supplier_field', args=[obj.pk, 'email'])
        )
    actions_link.short_description = 'Actions'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:supplier_id>/clear_field/<str:field_name>/', self.admin_site.admin_view(self.clear_field), name='clear_supplier_field'),
        ]
        return custom_urls + urls

    def clear_field(self, request, supplier_id, field_name):
        # Безопасная очистка поля
        obj = self.get_object(request, supplier_id)
        if obj is not None and hasattr(obj, field_name):
            setattr(obj, field_name, None)
            obj.save(update_fields=[field_name])
        from django.shortcuts import redirect
        return redirect(request.META.get('HTTP_REFERER', reverse('admin:app_supplier_change', args=[supplier_id])))

admin.site.register(Supplier, SupplierAdmin)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'level', 'supplier_link', 'debt_to_supplier', 'created_at')
    list_filter = ('city', 'country', 'level')
    search_fields = ('name', 'city', 'country', 'street', 'product_name', 'product_model')
    readonly_fields = ('created_at', 'level')

    fieldsets = (
        (None, {
            'fields': ('name', 'supplier', 'email', 'country', 'city', 'street', 'house_number',
                       'product_name', 'product_model', 'product_launch_date', 'debt_to_supplier')
        }),
        ('Технические', {'fields': ('created_at',)}),
    )

    # Ссылка на поставщика (для удобства на странице)
    def supplier_link(self, obj):
        if obj.supplier:
            url = admin.site.reverse('admin:network_networknode_change', args=[obj.supplier.pk])
            return f'<a href="{url}">{obj.supplier.name}</a>'
        return ''

    supplier_link.allow_tags = True
    supplier_link.short_description = 'Поставщик'

    # Кастомный action — очистить задолженность
    actions = ['clear_debt']

    def clear_debt(self, request, queryset):
        updated = queryset.update(debt_to_supplier=0)
        self.message_user(request, f'Задолженность очищена для {updated} объектов.')

    clear_debt.short_description = 'Очистить задолженность выбранных объектов'


@admin.register(NetworkObject)
class NetworkObjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city', 'supplier', 'debt']
    list_filter = ['city', 'supplier']  # Добавьте фильтрацию по городу и поставщику
    search_fields = ['name', 'supplier__name', 'city']  # Добавьте возможность поиска
    readonly_fields = ['debt']  # Сделайте поле задолженности только для чтения
