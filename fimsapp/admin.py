from .models import (
    User,
    Service,
    Statistics,
    MainCardSlider,
    WhyChooseUs,
    PatientTestimonial,
    ContactUs,
    Doctor,
)
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_staff', 'is_active', 'date_joined',)
    search_fields = ('email', 'first_name', 'last_name',)


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


class MainCardSliderAdmin(BaseModelAdmin):
    pass


class WhyChooseUsAdmin(BaseModelAdmin):
    pass


class PatientTestimonialAdmin(BaseModelAdmin):
    pass


class ContactUsAdmin(TimeBaseModelAdmin):
    list_display = ('mobile', 'email', 'address', 'facebook', 'twitter', 'instagram', 'linkedin', 'youtube',) + TimeBaseModelAdmin.list_display
    fieldsets = (
        (None, {
            'fields': ('mobile', 'email', 'address', 'facebook', 'twitter', 'instagram', 'linkedin', 'youtube', 'is_active')
        }),
        ('Time', {
            'fields': ('created_at', 'updated_at')
        }),
    )


class DoctorAdmin(TimeBaseModelAdmin):
    list_display = ('user', 'designation') + TimeBaseModelAdmin.list_display
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'designation')


admin.site.register(User, UserAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(MainCardSlider, MainCardSliderAdmin)
admin.site.register(WhyChooseUs, WhyChooseUsAdmin)
admin.site.register(PatientTestimonial, PatientTestimonialAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Doctor, DoctorAdmin)
