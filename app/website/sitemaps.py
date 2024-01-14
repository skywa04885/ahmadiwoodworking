from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from website.models import Post, Product, Project


class PostSitemap(Sitemap):
    priority = 0.2
    changefreq = "weekly"

    def items(self):
        return Post.objects.all()

    @staticmethod
    def lastmod(post: Post):
        return post.updated_at


class ProductSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Product.objects.all()

    @staticmethod
    def lastmod(product: Product):
        return product.updated_at


class ProjectSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return Project.objects.all()

    @staticmethod
    def lastmod(project: Project):
        return project.updated_at


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return ["index", "contact", "about", "portfolio", "products", "posts"]

    def location(self, item):
        return reverse(item)
