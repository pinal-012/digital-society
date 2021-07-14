"""digitalSociety URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='w_index'),
    path('register/', views.register, name='w_register'),

    path('profile/', views.profile, name='w_profile'),

    path('view-member/',views.view_member,name='w_view-member'),
    path('view-notice/',views.view_notice,name='w_view-notice'),
    path('view-event/',views.view_event,name='w_view-event'),
    path('view-photo/', views.view_photo, name='w_view-photo'),
    path('view-video/', views.view_video, name='w_view-video'),

    path('add-visitor/', views.add_visitor, name='w_add-visitor'),
    path('view-visitor/', views.view_visitor, name='w_view-visitor'),
    path('del-visitor/', views.del_visitor, name='w_del-visitor'),

    path('contact-list/',views.contact_list,name='w_contact-list'),

    ]