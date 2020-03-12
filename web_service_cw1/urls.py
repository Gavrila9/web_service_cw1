"""web_service_cw1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from rating_system.views import showMoudles,showRatings,showRatings4Moudles,register,login,loginOut,rate,showRatings4MoudlesYearSemester
urlpatterns = [
    path('admin/', admin.site.urls),
    path('rating/show/', showMoudles),
    path('rating/showRatings/', showRatings),
    path('rating/register/', register),
    path('rating/login/', login),
    path('rating/loginOut/', loginOut),
    path('rating/showRatings4Modules/', showRatings4Moudles),
    path('rating/rate/', rate),
    path('rating/showRatings4MoudlesYearSemester/', showRatings4MoudlesYearSemester),
]
