from django.conf.urls import url

from bookstore import views

urlpatterns = [
    url(r'^category/create', views.category_create, name='category-create'),
]