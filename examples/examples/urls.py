# Django
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
# Project
from index import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
