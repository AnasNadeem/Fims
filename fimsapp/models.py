from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .models_manager import UserManager

# Service - image, title, description, showinmaincard (bool)
# Statistics - image, title, description
# MainCardSlider - image, title, description
# MainCardService - service (fk)
# WhyChooseUs - image, title, description
# PatientTestimonial - image, title, description
# Contact Us - mobile, email, address, facebook, twitter, instagram, linkedin, youtube
# Doctor - user (fk), image, designation, description, services (m2m


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


class Service(TimeBaseModel):
    image = models.ImageField(upload_to='service')
    title = models.CharField(max_length=255)
    description = models.TextField()
    showinmaincard = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Statistics(TimeBaseModel):
    image = models.ImageField(upload_to='statistics')
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
    image = models.ImageField(upload_to='whychooseus')
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Why Choose Us'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class PatientTestimonial(TimeBaseModel):
    image = models.ImageField(upload_to='patienttestimonial')
    title = models.CharField(max_length=255)
    description = models.TextField()

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

    def __str__(self):
        return self.user.full_name()
