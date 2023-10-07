from .models import (
    User,
    UserOTP,
    Service,
    Statistics,
    MainCardSlider,
    WhyChooseUs,
    PatientTestimonial,
    ContactUs,
    Doctor,
    DoctorVideosSlider,
    DoctorOpdSchedule,
    DoctorYoutube,
    DoctorBlog,
)
from django.contrib import admin


class UserOTPInline(admin.TabularInline):
    model = UserOTP
    extra = 0


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_staff', 'is_active', 'date_joined',)
    search_fields = ('email', 'first_name', 'last_name',)
    inlines = (UserOTPInline,)


class TimeBaseModelAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'created_at', 'updated_at',)
    list_filter = ('is_active', 'created_at', 'updated_at',)
    readonly_fields = ('created_at', 'updated_at',)


class UserOTPAdmin(TimeBaseModelAdmin):
    list_display = ('user', 'otp', 'is_verified',) + TimeBaseModelAdmin.list_display
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'otp',)
    fieldsets = (
        ('User OTP', {
            'fields': ('user', 'otp', 'is_verified', 'is_active',)
        }),
        ('Time', {
            'fields': ('created_at', 'updated_at')
        }),
    )


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
        (None, {
            'fields': ('image', 'title', 'description', 'tags',)
        }),
        ('Additionals', {
            'fields': ('is_featured', 'showinmaincard', 'is_active')
        }),
        ('Time', {
            'fields': ('created_at', 'updated_at')
        }),
    )


class StatisticsAdmin(BaseModelAdmin):
    pass


class MainCardSliderAdmin(BaseModelAdmin):
    pass


class WhyChooseUsAdmin(BaseModelAdmin):
    pass


class PatientTestimonialAdmin(BaseModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('doctor', 'image', 'link', 'title', 'description', 'is_active')
        }),
        ('Time', {
            'fields': ('created_at', 'updated_at')
        }),
    )


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


class DoctorVideoSliderInline(admin.TabularInline):
    model = DoctorVideosSlider
    extra = 0


class DoctorOpdScheduleInline(admin.TabularInline):
    model = DoctorOpdSchedule
    extra = 1


class DoctorYoutubeInline(admin.TabularInline):
    model = DoctorYoutube
    extra = 0


class DoctorBlogInline(admin.TabularInline):
    model = DoctorBlog
    extra = 0


class DoctorAdmin(TimeBaseModelAdmin):
    list_display = ('user', 'designation') + TimeBaseModelAdmin.list_display
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'designation')
    list_filter = ('is_featured',) + TimeBaseModelAdmin.list_filter
    inlines = (DoctorOpdScheduleInline, DoctorVideoSliderInline, DoctorYoutubeInline, DoctorBlogInline)
    fieldsets = (
        (None, {
            'fields': ('user', 'image', 'designation', 'description', 'services', 'tags',)
        }),
        ('Additionals', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Time', {
            'fields': ('created_at', 'updated_at')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(UserOTP, UserOTPAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(MainCardSlider, MainCardSliderAdmin)
admin.site.register(WhyChooseUs, WhyChooseUsAdmin)
admin.site.register(PatientTestimonial, PatientTestimonialAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Doctor, DoctorAdmin)
