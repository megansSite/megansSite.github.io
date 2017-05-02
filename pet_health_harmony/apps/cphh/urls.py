from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^contact$', views.contact, name="contact"),
    url(r'^gallery$', views.gallery, name="gallery"),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^manage$', views.manage, name='manage'),
    url(r'^image/delete/(?P<id>\d+)$', views.destroy_image, name="destroy_image"),
    url(r'^image/approve/(?P<id>\d+)$', views.approve_image, name="approve_image"),
    url(r'^testimonial/delete/(?P<id>\d+)$', views.destroy_testimonial, name="destroy_testimonial"),
    url(r'^testimonial/approve/(?P<id>\d+)$', views.approve_testimonial, name="approve_testimonial"),    
]