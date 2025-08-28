from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name="Страна")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    street = models.CharField(max_length=255, blank=True, null=True, verbose_name="Улица")
    house_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер дома")
    debt = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    def __str__(self):
        return self.name


class NetworkObject(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, db_index=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="network_objects")
    debt = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    def __str__(self):
        return self.name


class NetworkNode(models.Model):
    """
    Модель для представления узлов сети.
    Узел сети может быть заводом, розничной сетью или индивидуальным предпринимателем.
    """

    LEVEL_CHOICES = (
        (0, "Завод"),
        (1, "Розничная сеть"),
        (2, "Индивидуальный предприниматель"),
    )

    name = models.CharField(max_length=255)

    email = models.EmailField(blank=True, null=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=200, blank=True, null=True)
    house_number = models.CharField(max_length=20, blank=True, null=True)
    level = models.IntegerField(choices=LEVEL_CHOICES, default=0)

    product_name = models.CharField(max_length=200, blank=True, null=True)
    product_model = models.CharField(max_length=200, blank=True, null=True)
    product_launch_date = models.DateField(blank=True, null=True)

    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subordinates",
        help_text="Предыдущий по иерархии узел (поставщик).",
    )

    debt_to_supplier = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0.00"))]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    level = models.PositiveSmallIntegerField(
        choices=LEVEL_CHOICES, editable=False, help_text="Уровень в цепочке: 0 — завод, 1 — розничная сеть, 2 — ИП"
    )

    class Meta:
        verbose_name = "Сеть (узел)"
        verbose_name_plural = "Сеть"

    def save(self, *args, **kwargs):
        if self.supplier is None:
            self.level = 0
        else:
            supplier_level = self.supplier.level if self.supplier.level is not None else 0
            self.level = min(supplier_level + 1, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (уровень {self.level})"


class Product(models.Model):
    """
    Модель продукта, представляющая товар в системе.
    """

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    network_objects = models.ManyToManyField(NetworkObject, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
