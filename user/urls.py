from django.urls import path
from user import views

urlpatterns = [
    path("register", views.RegisterRequestView.as_view(), name="register"),
    path("otp/<str:username>/<str:phone_number>", views.ValidateOtpView.as_view(), name="validate_otp_view"),
    path("login", views.LoginRequestView.as_view(), name="login"),
    path("logout", views.LogoutRequestView.as_view(), name="logout"),
    path('forget-password/', views.ForgetPasswordRequestView.as_view(), name='forget_password_request'),
    path('reset-password/<str:phone_number>/', views.ResetPasswordRequestView.as_view(), name='reset_password_request'),
    path("profile", views.ProfileView.as_view(), name="profile"),
    path("contact", views.ContactCreateView.as_view(), name="contact"),

]
