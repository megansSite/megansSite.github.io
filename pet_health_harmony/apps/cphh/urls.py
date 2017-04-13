from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^contact$', views.contact, name="contact"),
    url(r'^gallery$', views.gallery, name="gallery"),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^gallery/destroy(?P<id>\d+)$', views.destroy_image, name="destroy_image"),
]