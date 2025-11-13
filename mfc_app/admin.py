from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Category, User, Branch, Status, Service, Appointment, FavoriteService


class FavoriteServiceInline(admin.TabularInline):
    model = FavoriteService
    extra = 0
    raw_id_fields = ('user', 'service')

class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 0
    raw_id_fields = ('user', 'service', 'branch')
    readonly_fields = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'name')
    list_display_links = ('category_id', 'name')
    search_fields = ('name',)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('user_id', 'email', 'get_full_name', 'phone', 'created_at', 'is_staff')
    list_display_links = ('user_id', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    date_hierarchy = 'created_at'
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    @admin.display(description='Полное имя')
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = _('Полное имя')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('branch_id', 'name', 'address', 'phone', 'work_hours', 'display_photo', 'created_at')
    list_display_links = ('branch_id', 'name')
    list_filter = ('created_at',)
    search_fields = ('name', 'address', 'phone')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    @admin.display(description='Фото')
    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.photo.url)
        return "-"
    display_photo.short_description = _('Фото')

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('status_id', 'name')
    list_display_links = ('status_id', 'name')
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'name', 'category', 'state_duty', 'created_at')
    list_display_links = ('service_id', 'name')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    raw_id_fields = ('category',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    inlines = [FavoriteServiceInline]

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'appointment_id',
        'get_user_email',
        'get_service_name',
        'get_branch_name',
        'desired_date',
        'desired_time',
        'status',
        'created_at'
    )
    list_display_links = ('appointment_id',)
    list_filter = ('status', 'desired_date', 'created_at', 'branch')
    search_fields = ('user__email', 'service__name', 'branch__name')
    raw_id_fields = ('user', 'service', 'branch', 'status')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    @admin.display(description='Пользователь (email)')
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = _('Пользователь')

    @admin.display(description='Услуга')
    def get_service_name(self, obj):
        return obj.service.name if obj.service else "-"
    get_service_name.short_description = _('Услуга')

    @admin.display(description='Филиал')
    def get_branch_name(self, obj):
        return obj.branch.name if obj.branch else "-"
    get_branch_name.short_description = _('Филиал')

@admin.register(FavoriteService)
class FavoriteServiceAdmin(admin.ModelAdmin):
    list_display = ('favorite_service_id', 'user', 'service', 'created_at')
    list_display_links = ('favorite_service_id',)
    list_filter = ('created_at',)
    search_fields = ('user__email', 'service__name')
    raw_id_fields = ('user', 'service')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'