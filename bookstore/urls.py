from django.conf.urls import url

from bookstore import views

urlpatterns = [
    url(r'^category/create', views.category_create, name='category-create'),
    url(r'^category/edit/(?P<categ_id>[0-9]+)$',
        views.category_edit, name='category-edit'),
]