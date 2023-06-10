
from django.contrib import admin
from django.urls import path, include

import TodoApp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TodoApp.Application.urls')),
]
