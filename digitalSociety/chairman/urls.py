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
    path('', views.index, name='c_index'),
    path('login-page/', views.login_page, name='c_login-page'),
    path('check-email/',views.check_email, name='check-email'), 
    path('login-evaluate/', views.login_evaluate, name='c_login-evaluate'),
    path('logout/', views.logout, name='c_logout'),

    path('forgot-password/', views.forgot_password, name='c_forgot-password'),
    path('send-otp/', views.send_otp, name='c_send-otp'),
    path('reset-password/', views.reset_password, name='c_reset-password'),

    path('profile/', views.profile, name='c_profile'),
    path('profile-update/', views.profile_update, name='c_profile-update'),

    path('add-notice/', views.add_notice, name='c_add-notice'),
    path('view-notice/', views.view_notice, name='c_view-notice'),
    path('del-notice/', views.del_notice, name='c_del-notice'),

    path('add-event/', views.add_event, name='c_add-event'),
    path('view-event/', views.view_event, name='c_view-event'),
    path('del-event/', views.del_event, name='c_del-event'),
    
    path('add-member/', views.add_member, name='c_add-member'),
    path('view-member-profile/<int:pk>', views.view_member_profile, name='c_view-member-profile'),   #pk=primary key is sent with url
    path('view-member/',views.view_member,name='c_view-member'),
    path('del-member/', views.del_member, name='c_del-member'),
    path('update-member-profile/', views.update_member_profile, name='c_update-member-profile'),   #pk=primary key is sent with url
    
    path('watchman-list/',views.watchman_list,name='c_watchman-list'),
    path('watchman-approval/<int:pk>',views.watchman_approval,name='c_watchman-approval'),
    path('del-watchman/',views.del_watchman,name='c_del-watchman'),

    path('view-complaint/', views.view_complaint, name='c_view-complaint'),
    path('del-complaint/', views.del_complaint, name='c_del-complaint'),

    path('view-suggestion/', views.view_suggestion, name='c_view-suggestion'),
    path('del-suggestion/', views.del_suggestion, name='c_del-suggestion'),

    path('add-photo/', views.add_photo, name='c_add-photo'),
    path('view-photo/', views.view_photo, name='c_view-photo'),
    path('del-photo/', views.del_photo, name='c_del-photo'),
    path('add-video/', views.add_video, name='c_add-video'),
    path('view-video/', views.view_video, name='c_view-video'),
    path('del-video/', views.del_video, name='c_del-video'),

    path('view-visitor/',views.view_visitor,name='c_view-visitor'),
    path('contact-list/',views.contact_list,name='c_contact-list'),

    path('add-maintenance/', views.add_maintenance, name='c_add-maintenance'),
    path('view-maintenance/', views.view_maintenance, name='c_view-maintenance'),
    path('del-maintenance/', views.del_maintenance, name='c_del-maintenance'),
    

]
#path('view-event/', views.view_event, name='view-event'),