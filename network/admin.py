from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html

from .models import NetworkNode, NetworkObject, Product, Supplier


def reset_field(obj, field_name):
    """
    Очистка конкретного поля объекта.

    Args:
        obj: Экземпляр модели, поле которого нужно очистить.
        field_name: Имя поля, которое нужно очистить.
    """
    if hasattr(obj, field_name):
        setattr(obj, field_name, None)
        obj.save(update_fields=[field_name])


class SupplierAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления поставщиками.

    Позволяет выполнять CRUD операции над объектами Supplier.
    """

    list_display = ("name", "email", "country", "city", "street", "house_number", "actions_link")
    fieldsets = ((None, {"fields": ("name", "email", "country", "city", "street", "house_number")}),)

    def actions_link(self, obj):
        """
        Генерация ссылки для очистки поля долга.
        """
        return format_html(
            '<a class="button" href="{}">Очистить долг</a>',
            reverse("admin:clear_supplier_field", args=[obj.pk]),
        )

    actions_link.short_description = "Actions"

    def get_urls(self):
        """
        Получение URL-адресов для админ-панели.

        Returns:
            Список URL-адресов, включая пользовательские.
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:supplier_id>/clear_field/<str:field_name>/",
                self.admin_site.admin_view(self.clear_field),
                name="clear_supplier_field",
            ),
        ]
        return custom_urls + urls

    def clear_field(self, request, supplier_id, field_name):
        """
        Очистка поля поставщика по его ID.

        Args:
            request: HTTP-запрос.
            supplier_id: ID поставщика.
            field_name: Имя поля, которое нужно очистить.

        Returns:
            Перенаправление на страницу редактирования поставщика.
        """
        obj = self.get_object(request, supplier_id)
        if obj is not None and hasattr(obj, field_name):
            setattr(obj, field_name, None)
            obj.save(update_fields=[field_name])
        from django.shortcuts import redirect

        return redirect(request.META.get("HTTP_REFERER", reverse("admin:app_supplier_change", args=[supplier_id])))


admin.site.register(Supplier, SupplierAdmin)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления узлами сети.

    Позволяет выполнять CRUD операции над объектами NetworkNode.
    """

    list_display = ("name", "city", "country", "level", "supplier_link", "debt_to_supplier", "created_at")
    list_filter = ("city", "country", "level")
    search_fields = ("name", "city", "country", "street", "product_name", "product_model")
    readonly_fields = ("created_at", "level")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "supplier",
                    "email",
                    "country",
                    "city",
                    "street",
                    "house_number",
                    "product_name",
                    "product_model",
                    "product_launch_date",
                    "debt_to_supplier",
                )
            },
        ),
        ("Технические", {"fields": ("created_at",)}),
    )

    def supplier_link(self, obj):
        """
        Генерирует HTML-ссылку на поставщика узла сети.

        Args:
            obj (NetworkNode): Экземпляр узла сети, для которого создается ссылка.

        Returns:
            str: HTML-ссылка на страницу изменения поставщика, если поставщик существует, иначе пустая строка.
        """
        if obj.supplier:
            url = reverse("admin:network_networknode_change", args=[obj.supplier.pk])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "Нет поставщика"

    supplier_link.allow_tags = True
    supplier_link.short_description = "Поставщик"

    actions = ["clear_debt"]

    def clear_debt(self, request, queryset):
        """
        Очистка задолженности для выбранных узлов сети.

        Args:
            request (HttpRequest): HTTP запрос.
            queryset (QuerySet): Выбранные узлы сети для обновления.

        Returns:
            None: Выводит сообщение о количестве очищенных задолженностей.
        """
        updated = queryset.update(debt_to_supplier=0)
        self.message_user(request, f"Задолженность очищена для {updated} объектов.")

    clear_debt.short_description = "Очистить задолженность выбранных объектов"


@admin.register(NetworkObject)
class NetworkObjectAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления объектами сети.

    Позволяет выполнять CRUD операции над объектами NetworkObject.
    """

    list_display = ["id", "name", "city", "supplier", "debt"]
    list_filter = ["city", "supplier"]
    search_fields = ["name", "supplier__name", "city"]
    readonly_fields = ["debt"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административная панель для управления продуктами.
    """

    list_display = ("id", "name", "price", "supplier", "debt_to_supplier", "created_at", "display_network_objects")
    actions = ["clear_debt_to_supplier"]
    search_fields = (
        "name",
        "supplierr__name",
    )
    list_display_links = ["name", "supplier"]

    def display_network_objects(self, obj):
        """
        Метод для отображения связанных сетевых объектов в административной панели.
        """
        return ", ".join([str(network_object) for network_object in obj.network_objects.all()])

    display_network_objects.short_description = "Сетевые объекты"

    def clear_debt_to_supplier(self, request, queryset):
        """
        Действие для обнуления задолженности перед поставщиком для выбранных продуктов.
        """
        updated_count = queryset.update(debt_to_supplier=0)
        self.message_user(request, f"Задолженность перед поставщиком для {updated_count} продукта(ов) была обнулена.")

        clear_debt_to_supplier.short_description = "Обнулить задолженность перед поставщиком для выбранных продуктов"
