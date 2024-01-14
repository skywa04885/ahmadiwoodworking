from django.urls import path
from django.contrib.sitemaps.views import sitemap

from . import views
from website.sitemaps import PostSitemap, ProductSitemap, ProjectSitemap, StaticViewSitemap


sitemaps = {
    "posts": PostSitemap,
    "products": ProductSitemap,
    "projects": ProjectSitemap,
    "static": StaticViewSitemap
}

urlpatterns = [
    path("", views.index, name="index"),
    path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
    path('portfolio', views.portfolio, name='portfolio'),
    path('project/<int:project_id>', views.project, name='project'),
    path('product/<int:product_id>', views.product, name='product'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('request_consultation_form', views.request_consultation, name='request_consultation'),
    path('products', views.products, name='products'),
    path('newest_projects', views.posts, name='newest_projects'),
    path('posts', views.posts, name='posts'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]
