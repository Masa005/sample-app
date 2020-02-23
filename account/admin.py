from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'birthday', 'email',
                  'name')


# Register your models here.
@admin.register(User)
class AdminUserAdmin(UserAdmin):
    add_form = AdminUserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'birthday', 'email',
                           'name')}),
    )
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': (
        'username', 'birthday', 'email', 'name', 'password1',
        'password2'), }),)
    list_display = ('username', 'email', 'name', 'birthday', 'is_staff')
    search_fields = ('username', 'name', 'email', 'birthday')
    filter_horizontal = ('groups', 'user_permissions')
