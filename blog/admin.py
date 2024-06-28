from django.contrib import admin
from .models import User, Category, Post, Tag


class HomeAdmin(admin.ModelAdmin):
    list_display = ('username', 'image', 'email',)


admin.site.register(User, HomeAdmin)
admin.site.register(Post)
admin.site.register(Tag)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ("name",)
        }),
    )

    list_display = ["name", "slug"]
    search_fields = ("name",)
