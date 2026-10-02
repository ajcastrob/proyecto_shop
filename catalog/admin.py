from django.contrib import admin
from catalog.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ["category"]
    prepopulated_fields = {"slug": ["title"]}
    actions = ["clear_inventory"]
    list_display = ["title", "price", "inventory_status", "category_title"]
    list_editable = ["price"]
    list_filter = ["category", "last_update"]
    list_per_page = 10
    list_select_related = ["category"]

    @admin.display(ordering="inventory", description="Estado de inventario")
    def inventory_status(self, product):
        if product.inventory < 100:
            return "Low"
        return "Ok"

    @admin.display(ordering="category__title", description="Categoría")
    def category_title(self, product):
        return product.category.title

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(
            request, f"{update_count} producto fue actualizado correctamente"
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]
