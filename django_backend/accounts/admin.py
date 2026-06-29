from django.contrib import admin

from .models import Role, User, UserRoleMapping

admin.site.site_header = 'Talentime Administration'
admin.site.site_title = 'Talentime Admin'
admin.site.index_title = 'Administration Database Controller'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'slug')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'country', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone')


@admin.register(UserRoleMapping)
class UserRoleMappingAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_primary', 'is_active', 'assigned_at')
    list_filter = ('role', 'is_primary', 'is_active')
