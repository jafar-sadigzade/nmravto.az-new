from django.urls import path
from carsaleapp import views

urlpatterns = [
    path("", views.cars_request, name=""),
    path("home", views.cars_request, name="home"),
    path("index", views.cars_request, name="index"),
    path("cars", views.cars_request, name="cars"),

    path("caradd", views.caradd, name="caradd"),
    path("car_details/<int:id>", views.car_detailed_views, name="car_details"),
    path("caredit/<int:id>", views.careditviews, name="caredit"),

    path("favorites", views.favorites_list, name="favorites_list"),
    path("favorites/<int:id>/", views.favorites_add, name="favorites_add"),

    path("elanlar", views.carads_list, name="elanlar"),
    path("elanlar/<int:id>", views.carads_remove, name="carads_remove"),

    path("searchcar", views.searchcar, name="searchcar"),
    path("comment/<int:id>", views.carcomment_add, name="carcomment_add"),
]
