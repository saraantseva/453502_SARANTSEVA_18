from django.contrib import admin
from core.models import *
from django.contrib import admin
from .models import *
from django.contrib import admin
from .models import *


# БАЗОВЫЕ СПРАВОЧНИКИ (простая регистрация)

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(SparePartType)
class SparePartTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']



# ОСНОВНЫЕ МОДЕЛИ

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'birth_date', 'created_at']
    list_filter = ['created_at']
    search_fields = ['full_name', 'phone']
    date_hierarchy = 'created_at'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'get_specializations', 'created_at']
    list_filter = ['specialization', 'created_at']
    search_fields = ['full_name', 'phone']
    filter_horizontal = ['specialization']

    def get_specializations(self, obj):
        return ", ".join([s.name for s in obj.specialization.all()])
    get_specializations.short_description = "Специализации"


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'client', 'device_type', 'created_at']
    list_filter = ['device_type', 'client', 'created_at']
    search_fields = ['brand', 'model', 'serial_number']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'price', 'duration_days']
    list_filter = ['service_type', 'price']
    search_fields = ['name']


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ['name', 'part_type', 'price', 'quantity_in_stock']
    list_filter = ['part_type', 'price']
    search_fields = ['name']



# ЗАКАЗЫ (с встроенным редактированием)

class OrderServiceInline(admin.TabularInline):
    model = OrderService
    extra = 1
    fields = ['service', 'quantity', 'price_at_time']


class OrderSparePartInline(admin.TabularInline):
    model = OrderSparePart
    extra = 1
    fields = ['spare_part', 'quantity', 'price_at_time']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'client', 'status', 'created_at', 'total_cost']
    list_filter = ['status', 'created_at', 'employee']
    search_fields = ['order_number', 'client__full_name']
    date_hierarchy = 'created_at'
    inlines = [OrderServiceInline, OrderSparePartInline]
    readonly_fields = ['total_cost']
    fieldsets = (
        ('Основное', {
            'fields': ('order_number', 'client', 'device', 'employee', 'status')
        }),
        ('Финансы', {
            'fields': ('total_cost',)
        }),
        ('Прочее', {
            'fields': ('client_problem', 'master_note', 'completion_date')
        }),
    )


# СТРАНИЦЫ САЙТА (простые модели)
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title']

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('text', 'logo', 'requisites', 'video_url')
        }),
    )

@admin.register(Glossary)
class GlossaryAdmin(admin.ModelAdmin):
    list_display = ['term', 'created_at']
    list_filter = ['created_at']
    search_fields = ['term']

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title']

@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'is_active', 'expires_at', 'created_at']
    list_filter = ['is_active', 'discount_percent']
    search_fields = ['code']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'text']
