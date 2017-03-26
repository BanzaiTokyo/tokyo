from django.contrib.sitemaps import Sitemap
from askapp.models import Thread, User
from django.template.defaultfilters import slugify


class ThreadSitemap(Sitemap):
    """
    What does this class do?
    """

    #what is changefreq?
    changefreq = "never"

    priority = 0.5

    def items(self):
        return Thread.objects.filter(deleted=False).order_by('-created')

    def lastmod(self, obj):
        return obj.created

    def location(self, obj):
        return '/thread/{}/{}/'.format(obj.id, slugify(obj))


class ProfileSitemap(Sitemap):
    """
    Some documentation would be helpful
    """
    changefreq = "never"
    priority = 0.5

    def items(self):
        return User.objects.filter(is_active=True).order_by('-date_joined')

    def lastmod(self, obj):
        return obj.date_joined

    def location(self, obj):
        return '/profile/{}/{}/'.format(obj.id, slugify(obj))

# what does this dictionary do?
sitemap_dict = {
    'threads': ThreadSitemap,
    'profiles': ProfileSitemap,
}