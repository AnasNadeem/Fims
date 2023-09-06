from .models import (
    Service,
    Statistics,
    MainCardSlider,
    WhyChooseUs,
    PatientTestimonial,
    ContactUs,
)
from django.contrib import admin


class TimeBaseModelAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'created_at', 'updated_at',)
    list_filter = ('is_active', 'created_at', 'updated_at',)
    readonly_fields = ('created_at', 'updated_at',)


class BaseModelAdmin(TimeBaseModelAdmin):
    list_display = ('title', 'image',) + TimeBaseModelAdmin.list_display
    search_fields = ('title',)
    fieldsets = (
        (None, {
            'fields': ('image', 'title', 'description', 'is_active')
        }),
        ('Time', {
            'fields': ('created_at', 'updated_at')
        }),
    )


class ServiceAdmin(BaseModelAdmin):
    list_display = BaseModelAdmin.list_display + ('showinmaincard',)
    list_filter = ('showinmaincard',) + BaseModelAdmin.list_filter
    fieldsets = (
        ('Additionals', {
            'fields': ('showinmaincard',)
        }),
    ) + BaseModelAdmin.fieldsets


class StatisticsAdmin(BaseModelAdmin):
    pass


admin.site.register(Service, ServiceAdmin)
admin.site.register(Statistics, StatisticsAdmin)