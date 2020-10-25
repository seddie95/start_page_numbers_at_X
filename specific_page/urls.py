"""specific_page URL Configuration

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
from django.contrib import admin
from django.urls import path
from pages import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('process/', views.ProcessView.as_view(), name='process'),
    path('download/', views.DownloadView.as_view(), name='download'),
    path('delete/', views.DeleteView.as_view(), name='delete'),
    path('reupload/', views.FileDeleted.as_view(), name='reupload'),
    path('help/', views.HelpView.as_view(), name='help'),
    path('404/', views.error_404_view, name='404')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = 'pages.views.error_404_view'

handler500 = 'pages.views.error_500_view'
