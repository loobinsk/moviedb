from django.contrib.sitemaps import Sitemap
from .models import Compilation

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Compilation.objects.all()

    def lastmod(self, obj):
        return obj.created
