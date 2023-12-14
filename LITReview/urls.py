"""
URL configuration for LITReview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
import users.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', users.views.login_page, name='login'),
    path('signup', users.views.signup_page, name='signup'),
    path('logout', users.views.logout_page, name='logout'),
    path('flux', blog.views.flux_page, name='flux'),
    path('ticket', blog.views.ticket_page, name='ticket'),
]
