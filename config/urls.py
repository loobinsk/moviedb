from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from objects.sitemaps import PostSitemap
from django.views.generic.base import TemplateView

sitemaps = {
    'objects': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('form/', include('objects.urls')),
    path('', include('home.urls')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "config.views.page_not_found_view"