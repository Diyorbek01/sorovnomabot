from django.db import models

from shared.models import BaseModel


# Create your models here.


class User(BaseModel):
    tg_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    is_human = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Variant(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @property
    def number_votes(self):
        return Vote.objects.filter(variant_id=self.id).count()


class Sorovnoma(BaseModel):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sorovnoma")
    image = models.ImageField(upload_to="images/")
    description = models.TextField()
    variants = models.ManyToManyField(Variant, blank=True)
    deadline = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

    @property
    def number_of_votes(self):
        total_votes = 0
        for i in self.variants.all():
            total_votes += i.voting.count()
        return total_votes


class Vote(BaseModel):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='voting')
    sorovnoma = models.ForeignKey(Sorovnoma, on_delete=models.CASCADE, related_name='voting')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.variant.name


class RequiredChannel(BaseModel):
    username = models.CharField(max_length=255)
    sorovnoma = models.ForeignKey(Sorovnoma, on_delete=models.CASCADE, related_name="channels")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_channels")
    number_of_joined_users = models.BigIntegerField(default=0)
    number_of_planed_users = models.BigIntegerField(default=0)
    is_active = models.BooleanField(default=True)
