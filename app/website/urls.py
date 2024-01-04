from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact", views.contact, name="contact"),
    path("about", views.about, name="about"),
    path('contact-thanks', views.contact_thanks, name='contact-thanks'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('project/<int:project_id>', views.project, name='project'),
    path('product/<int:product_id>', views.product, name='product')
]
