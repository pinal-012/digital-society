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
    path('', views.index, name='index'),

    path('view-notice/', views.view_notice, name='view-notice'),
    
    path('add-event/', views.add_event, name='add-event'),
    path('view-event/', views.view_event, name='view-event'),
    path('view-your-event/', views.view_your_event, name='view-your-event'),
    path('del-event/', views.del_event, name='del-event'),

    path('profile/', views.profile, name='profile'),
    path('profile-update/', views.profile_update, name='profile-update'),

    path('add-complaint/',views.add_complaint,name='add-complaint'),
    path('view-complaint/',views.view_complaint,name='view-complaint'),
    path('del-complaint/',views.del_complaint,name='del-complaint'),


    path('add-suggestion/',views.add_suggestion,name='add-suggestion'),
    path('view-suggestion/',views.view_suggestion,name='view-suggestion'),
    path('del-suggestion/',views.del_suggestion,name='del-suggestion'),

    path('view-member/',views.view_member,name='view-member'),
    path('view-member-profile/<int:pk>',views.view_member_profile,name='view-member-profile'),

    path('view-photo/',views.view_photo,name='view-photo'),
    path('view-video/',views.view_video,name='view-video'),

    path('view-visitor/',views.view_visitor,name='view-visitor'),
    path('contact-list/',views.contact_list,name='m_contact-list'),

    path('maintenance-bill/',views.maintenance_bill,name='maintenance-bill'),

    path('initiate-payment/<int:pk>', views.initiate_payment, name='initiate-payment'),
    path('callback/', views.callback, name='callback'),
   
    


]
#
#path('view-event/', views.view_event, name='view-event'),
#
#urlpatterns = [
   # path('', views.index, name='index'),
   # path('login-page/', views.login_page, name='login-page'),
   # path('login-evaluate/', views.login_evaluate, name='login-evaluate'),
   # path('logout/', views.logout, name='logout'),
#
   # path('forgot-password/', views.forgot_password, name='forgot-password'),
   # path('send-otp/', views.send_otp, name='send-otp'),
   # path('reset-password/', views.reset_password, name='reset-password'),
#
   # path('profile/', views.profile, name='profile'),
   # path('profile-update/', views.profile_update, name='profile-update'),
#
   # path('add-notice-page/', views.add_notice_page, name='add-notice-page'),
   # path('add-notice/', views.add_notice, name='add-notice'),
   # path('view-notice/', views.view_notice, name='view-notice'),
#
   # path('add-event-page/', views.add_event_page, name='add-event-page'),
   # path('add-event/', views.add_event, name='add-event'),
   # path('view-event/', views.view_event, name='view-event'),
   # 
   # path('add-member-page/', views.add_member_page, name='add-member-page'),
   # path('add-member/', views.add_member, name='add-member'),
   # path('view-member-profile/<int:pk>', views.view_member_profile, name='view-member-profile'),   #pk=primary key is sent with url
   # path('view-member/',views.view_member,name='view-member'),
   # 
#
#]#