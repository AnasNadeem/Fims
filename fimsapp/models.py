from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from .models_manager import UserManager


class TimeBaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=10, null=True, blank=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


class UserOTP(TimeBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class Service(TimeBaseModel):
    image = models.FileField(upload_to='service')
    title = models.CharField(max_length=255)
    description = models.TextField()
    showinmaincard = models.BooleanField(default=False)
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Statistics(TimeBaseModel):
    image = models.FileField(upload_to='statistics')
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Statistics'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class MainCardSlider(TimeBaseModel):
    image = models.ImageField(upload_to='maincardslider')
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Main Card Sliders'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


# class MainCardService(TimeBaseModel):
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.service.title


class WhyChooseUs(TimeBaseModel):
    image = models.FileField(upload_to='whychooseus')
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Why Choose Us'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class PatientTestimonial(TimeBaseModel):
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='patienttestimonial')
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = 'Patient Testimonials'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class ContactUs(TimeBaseModel):
    mobile = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.TextField()
    facebook = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    instagram = models.CharField(max_length=255, blank=True)
    linkedin = models.CharField(max_length=255, blank=True)
    youtube = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'Contact Us'
        ordering = ('-created_at',)

    def __str__(self):
        return self.email


class Doctor(TimeBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='doctor')
    designation = models.CharField(max_length=255)
    description = models.TextField()
    services = models.ManyToManyField(Service)
    is_featured = models.BooleanField(default=False)
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)

    def __str__(self):
        return self.user.full_name()


class DoctorVideosSlider(TimeBaseModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    link = models.URLField()
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.doctor.user.full_name()


class DoctorOpdSchedule(TimeBaseModel):
    DAYS_CHOICES = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday')
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.CharField(max_length=255, choices=DAYS_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.doctor.user.full_name()} - {self.day}'


class DoctorYoutube(TimeBaseModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    link = models.URLField()
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f'{self.doctor.user.full_name()} - {self.title}'


class DoctorBlog(TimeBaseModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    link = models.URLField()
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f'{self.doctor.user.full_name()} - {self.title}'
