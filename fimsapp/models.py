from django.db import models

# Service - image, title, description, showinmaincard (bool)
# Statistics - image, title, description
# MainCardSlider - image, title, description
# MainCardService - service (fk)
# WhyChooseUs - image, title, description
# PatientTestimonial - image, title, description
# Contact Us - mobile, email, address, facebook, twitter, instagram, linkedin, youtube

class TimeBaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


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

    def __str__(self):
        return self.title


class MainCardSlider(TimeBaseModel):
    image = models.ImageField(upload_to='maincardslider')
    title = models.CharField(max_length=255)
    description = models.TextField()

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

    def __str__(self):
        return self.title


class PatientTestimonial(TimeBaseModel):
    image = models.ImageField(upload_to='patienttestimonial')
    title = models.CharField(max_length=255)
    description = models.TextField()

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

    def __str__(self):
        return self.email
