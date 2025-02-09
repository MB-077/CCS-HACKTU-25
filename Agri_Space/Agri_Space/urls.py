"""
URL configuration for Agri_Space project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language
from schema_graph.views import Schema

admin.site.site_header = "Agri Space Admin"
admin.site.site_title = "Agri Space"
admin.site.index_title = "Welcome to the Agri Space"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Users.urls')),
    path('schema/', Schema.as_view()),
    path('telephony/', include('telephony.urls')),
    path('ml_model/', include('Ml_model.urls')),
    path('translate/', include('translation.urls')),
    path('sensors/', include('Sensors.urls')),
    path('i18n/', set_language, name='set_language'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)