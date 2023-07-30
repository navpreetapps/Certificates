from django.urls import path
from . import views

urlpatterns = [
    path('tester/', views.tester, name='tester'),
    path('home/', views.home, name='home'),
    path('builder/', views.builder, name='builder'),
    path('verifier/', views.verifier, name='verifier'),
    path('sign-in/', views.sign_in, name='signin'),
    path('sign-up/', views.sign_up, name='signup'),
    path('add-certs/', views.add_certs, name='add_certs'),
    path('signup-saver', views.signup_saver, name='signup_saver'),
    path('login-checker', views.login_checker, name='login_checker'),
    path('certificate-verifier', views.verify_token, name='verify_token'),
    path('previewpdf', views.previewpdf, name='previewpdf'),
    path('savepdf', views.savepdf, name='savepdf'),
    path('style-previewer', views.style_previewer, name='style_previewer'),
    path('style-storer', views.style_storer, name='style_storer'),
]