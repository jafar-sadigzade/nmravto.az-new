from django.contrib import admin
from carsaleapp.models import Comment, CarDetail, CarAdditionalSpecification, CarSpecification, CarPricing, CarImage, CarMultipleImage, CarFavorite


@admin.register(CarAdditionalSpecification)
class AdminCarAddInfo(admin.ModelAdmin):
    list_display = ['id', 'option']
    search_fields = ['option']
    ordering = ['id']


@admin.register(CarDetail)
class AdminCar(admin.ModelAdmin):
    list_display = ['user', 'brand', 'model', 'year', 'publish_date', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active', 'publish_date', 'brand']
    search_fields = ['brand', 'model', 'user__email']
    ordering = ['-publish_date', 'user']


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['user', 'car', 'publish_date']
    list_filter = ['publish_date', 'user']
    search_fields = ['user__email', 'car__brand', 'car__model']
    ordering = ['-publish_date']


@admin.register(CarSpecification)
class AdminCarSpecification(admin.ModelAdmin):
    list_display = ['car', 'gearbox', 'mileage']
    search_fields = ['car__brand', 'car__model']
    ordering = ['car']


@admin.register(CarPricing)
class AdminCarPricing(admin.ModelAdmin):
    list_display = ['car', 'price', 'priceunit']
    search_fields = ['car__brand', 'car__model']
    ordering = ['car']


@admin.register(CarImage)
class AdminCarImage(admin.ModelAdmin):
    list_display = ['car']
    search_fields = ['car__brand', 'car__model']
    ordering = ['car']


@admin.register(CarMultipleImage)
class AdminCarMultipleImage(admin.ModelAdmin):
    list_display = ['car']
    search_fields = ['car__brand', 'car__model']
    ordering = ['car']


@admin.register(CarFavorite)
class AdminCarFavorite(admin.ModelAdmin):
    list_display = ['car']
    search_fields = ['car__brand', 'car__model']
    ordering = ['car']
