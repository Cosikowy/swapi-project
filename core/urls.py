"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from data_explorer.views import (
    collecion_view,
    historical_data,
    occurrence_count,
    update,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("collection/", collecion_view, name="collecion-view"),
    path("", historical_data, name="collecions-view"),
    path("occurrence-counter/<str:id>/", occurrence_count, name="fields-count-view"),
    path("update/", update, name="collections-update"),
]
