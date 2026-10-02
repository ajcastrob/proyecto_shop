from django.contrib import admin
from catalog.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ["category"]
    prepopulated_fields = {"slug": ["title"]}
    actions = ["clear_inventory"]
    list_display = ["title", "price", "inventory_status", "collection_title"]
    list_editable = ["price"]
    list_filter = ["category", "last_update"]
    list_per_page = 10
    list_select_related = ["category"]

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 100:
            return "Low"
        return "Ok"

    def collection_title(self, product):
        return product.category.title

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(request, f"{update_count} products were successfully updated")


@admin.register(Category)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]
