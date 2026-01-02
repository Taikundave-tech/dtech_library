"""
URL configuration for dtech_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path,include
from django.contrib.auth import views as auth_views
from library_mgmt import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth
    path('accounts/',include('django.contrib.auth.urls')),
    
    # App
    path('',views.dashboard,name='dashboard'),
    path('register/',views.register,name='register'),
    path('book/',views.book_session, name='book_session'),
    path('end-session/<int:session_id>/',views.end_session,name='end_session'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('reports/',views.reports,name='reports'),
    path('books/', views.book_list_view, name='book_list'),
]

