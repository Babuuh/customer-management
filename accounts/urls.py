from django.urls import path

from django.contrib.auth import views as auth_views
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customers/<str:pk>/',views.customers, name='customers'),
    path('create_order/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.updateOrder, name='delete_order'),

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('user/', views.userPage, name='user_page'),
    path('settings/', views.accountSettings, name='settings'),

    #password management
    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
        name='password_reset'),
    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),
        name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'),
        name='password_reset_confirm'),
    path('reset_password/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)