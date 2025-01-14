from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _

from .forms import UserCreationForm
from .models import Model, ModelImages, User


class ModelAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "country",
        "city",
        "height",
        "bust",
        "waist",
        "hips",
    )
    list_filter = (
        "country",
        "hair",
        "eye_color",
    )
    search_fields = ["full_name"]


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (_("Permissions"), {"fields": ["is_active"]}),
        (_("Important dates"), {"fields": ["date_joined"]}),
    )
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "is_staff",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    ordering = ("email",)


admin.site.register(Model, ModelAdmin)
admin.site.register(ModelImages)
