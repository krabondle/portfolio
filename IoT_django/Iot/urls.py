"""iotsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from mysite import views

from django.conf.urls import include

#靜態文件
from django.views import static
from django.conf import settings
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'), #靜態文件
    path('', views.Navigation),
    path('Community/', views.index, name='Index'),
    #path('add/',views.add, name='add'),
    path('accounts/', include('allauth.urls')),
    #path('Navigation/', views.Navigation, name='Navigation'),
    path('Smarthome/', views.Smarthome, name='Smarthome'),
    path('Smartoffice/',views.Smartoffice, name= 'Smartoffice'),
    path('Smartparking/',views.Smartparking, name= 'Smartparking'),

    path('mqtt_publisher/',views.mqtt_publisher, name='mqtt_publisher'),
    path('Node_red/', views.Node_red, name='Node_red'),
    path('Node-Red_dashboard/', views.NodeRed_dashboard, name='Node-Red_dashboard'),
    path('stream/', views.livefe),
    path('ipcamera/', views.ipcamera),
    path('detail/', views.detail.as_view(), name= 'detail'),
    path('search_post/',views.detail.search_post, name='search_post'),
    path('data_update/',views.data_update, name='data_update'),

    path('detail_<str:sensor>/', views.detail.as_view(), name='detail'),
    path('detail_<str:sensor>/<str:date>/', views.detail.as_view(), name='detail'),
    path('detail_A00101/', views.detail.as_view(), name='detail_A00101'),
    path('detail_A00102/', views.detail.as_view(), name='detail_A00102'),
    path('detail_A10101/', views.detail.as_view(), name='detail_A10101'),
    path('detail_A20101/', views.detail.as_view(), name='detail_A20101'),
    path('detail_A20102/', views.detail.as_view(), name='detail_A20102'),
    path('detail_A20103/', views.detail.as_view(), name='detail_A20103'),
    path('detail_A30101/', views.detail.as_view(), name='detail_A30101'),
    path('detail_A40101/', views.detail.as_view(), name='detail_A40101'),
    path('detail_A50101/', views.detail.as_view(), name='detail_A50101'),
    path('detail_A60101/', views.detail.as_view(), name='detail_A60101'),
    path('detail_A70101/', views.detail.as_view(), name='detail_A70101'),
    path('detail_A80101/', views.detail.as_view(), name='detail_A80101'),
    path('detail_A90101/', views.detail.as_view(), name='detail_A90101'),
    path('detail_B00101/', views.detail.as_view(), name='detail_B00101'),
    path('detail_B10101/', views.detail.as_view(), name='detail_B10101'),
    path('detail_B20101/', views.detail.as_view(), name='detail_B20101'),
    path('detail_B30101/', views.detail.as_view(), name='detail_B30101'),

    #path('api/data/', views.get_data, name='api-data'),
    #path('api/chart/data/', views.ChartData.as_view(), name='api-data'),
    #path('chart/', views.HomeView.as_view(), name='chart'),
] 

'''
urlpatterns += [
    #path('mysite/', include('mysite.urls')),
    
    #path('', RedirectView.as_view(url='/mysite/', permanent=True)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''