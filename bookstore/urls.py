from django.conf.urls import url

from bookstore import views

urlpatterns = [
    url(r'^category/create', views.category_create, name='category-create'),
    url(r'^category/edit/(?P<categ_id>[0-9]+)$',
        views.category_edit, name='category-edit'),
    url(r'^category/delete/(?P<categ_id>[0-9]+)$',
        views.category_delete, name='category-delete'),
    url(r'^book/create', views.book_create, name='book-create'),
    url(r'^book/edit/(?P<book_id>[0-9]+)$',
        views.book_edit, name='book-edit'),
]