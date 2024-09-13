from django.db import models
from user.models import NewUser


class CarDetail(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True, blank=True)

    USAGE_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]
    usage = models.CharField(max_length=9, choices=USAGE_CHOICES, blank=True, null=True)
    brand = models.CharField(verbose_name="marka", max_length=20, blank=True, null=True)
    model = models.CharField(verbose_name="model", max_length=23, blank=True, null=True)
    ban = models.CharField(verbose_name="ban növü", max_length=15, blank=True, null=True)
    color = models.CharField(verbose_name="rəng", max_length=15, blank=True, null=True)
    fuel = models.CharField(verbose_name="yanacaq növü", max_length=15, blank=True, null=True)
    year = models.CharField(verbose_name="buraxılış ili", max_length=4, null=True, blank=True)
    market = models.CharField(verbose_name="bazar", max_length=15, blank=True, null=True)
    seats = models.CharField(verbose_name="oturacaq sayı", max_length=13, blank=True, null=True)
    credit = models.BooleanField(verbose_name="Kredit mövcuddurmu?", default=False)
    swap = models.BooleanField(verbose_name="Barter mövcuddurmu?", default=False)
    addinfo = models.TextField(verbose_name="Əlavə məlumat", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_comment = models.BooleanField(default=True)
    publish_date = models.DateTimeField(verbose_name="Yayınlanma tarixi: ", auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Avtomobil'
        verbose_name_plural = 'Avtomobillər'
        ordering = ['-publish_date', 'id']

    def __str__(self):
        return f"{self.user} {self.brand} {self.model}"


class CarAdditionalSpecification(models.Model):
    option = models.CharField(max_length=50, unique=True, verbose_name="Xüsusiyyət")

    class Meta:
        verbose_name = 'Əlavə təchizat'
        verbose_name_plural = 'Əlavə təchizat'

    def __str__(self):
        return f"{self.option}"


class CarSpecification(models.Model):
    car = models.OneToOneField(CarDetail, on_delete=models.CASCADE, related_name='specifications')
    gearbox = models.CharField(verbose_name="ötür", max_length=20, blank=True, null=True)
    mileage = models.IntegerField(verbose_name="getdiyi yol", null=True, blank=True)
    distanceunit = models.CharField(max_length=5, null=True, blank=True)
    volume = models.IntegerField(verbose_name="mator həcmi", null=True, blank=True)
    power = models.IntegerField(verbose_name="at gücü", null=True, blank=True)
    condition = models.TextField(verbose_name="vəziyyəti", null=True, blank=True)
    additional_information = models.ManyToManyField(CarAdditionalSpecification, related_name="additional_information",
                                                    blank=True)

    class Meta:
        verbose_name = 'Avtomobil xüsusiyyətləri'
        verbose_name_plural = 'Avtomobillərin xüsusiyyətləri'

    def __str__(self):
        return f"{self.car}: avtomobilinin xüsusiyyətləri"


class CarPricing(models.Model):
    car = models.OneToOneField(CarDetail, on_delete=models.CASCADE, related_name='pricing')
    price = models.IntegerField(verbose_name="qiymət", null=True, blank=True)
    priceunit = models.CharField(max_length=8, null=True, blank=True)

    class Meta:
        verbose_name = 'Avtomobilin qiyməti'
        verbose_name_plural = 'Avtomobillərin qiyməti'

    def __str__(self):
        return f"{self.car} avtomobilinin qiyməti"


class CarImage(models.Model):
    car = models.OneToOneField(CarDetail, on_delete=models.CASCADE, related_name='images')
    front = models.ImageField(upload_to="front/")
    side = models.ImageField(upload_to="side/")
    interior = models.ImageField(upload_to="interior/")

    class Meta:
        verbose_name = 'Avtomobilin şəkilləri'
        verbose_name_plural = 'Avtomobillərin şəkilləri'

    def __str__(self):
        return f"{self.car} avtomobilinin şəkilləri"


class CarMultipleImage(models.Model):
    car = models.ForeignKey(CarDetail, on_delete=models.CASCADE, related_name='multiple_images', null=True, blank=True)
    images = models.FileField(upload_to='car_additional_images/')

    class Meta:
        verbose_name = 'Əlavə şəkil'
        verbose_name_plural = 'Əlavə şəkil'

    def __str__(self):
        return f"{self.car}"


class CarFavorite(models.Model):
    car = models.OneToOneField(CarDetail, on_delete=models.CASCADE, related_name='favorites')
    favorites = models.ManyToManyField(NewUser, related_name="favorites", blank=True)

    class Meta:
        verbose_name = 'Seçdiklərim'
        verbose_name_plural = 'Seçdiklərim'

    def __str__(self):
        return f"{self.car}"


class Comment(models.Model):
    car = models.ForeignKey(CarDetail, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("publish_date",)
        verbose_name = 'Rəy'
        verbose_name_plural = 'Rəy'

    def __str__(self):
        return f"{self.user}"
