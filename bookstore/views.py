from django.shortcuts import render
from django.http import HttpResponse

from bookstore import forms, models

# Create your views here.


def category_create(request):
    context = {
        'category_form': forms.CategoryForm(),
        'categories': models.Category.objects.all()
    }

    if 'name' in request.POST:
        forms.CategoryForm(request.POST).save()

        context['categories'] = models.Category.objects.all()
        context['feedback'] = 'Category: {0} created!'.format(request.POST['name'])

        return render(request, 'category-create.html', context, status=201)
    return render(request, 'category-create.html', context)


def category_edit(request, categ_id):
    edit_obj = models.Category.objects.get(pk=categ_id)
    context = {
        'category_form': forms.CategoryForm(initial={'name': edit_obj.name}),
        'categ_id': categ_id
    }
    if 'name' in request.POST:

        edit_obj.name = request.POST['name']
        edit_obj.save()

        context['feedback'] = 'Category of id {0} has been edited\
            successfully!'.format(edit_obj.id)
        return render(request, 'category-edit.html', context)
    return render(request, 'category-edit.html', context)


def category_delete(request, categ_id):
    context = {
        'categ_id': categ_id
    }
    try:
        context['category'] = models.Category.objects.get(pk=categ_id)
        if request.method == 'POST':
            context['category'].delete()
            context['category'] = None
            return render(request, 'category-delete.html', context)
    except models.Category.DoesNotExist:
        context['category'] = None
    return render(request, 'category-delete.html', context)


def book_create(request):
    context = {
        'books': models.Book.objects.all(),
        'book_form': forms.BookForm()
    }
    if request.POST:
        new_book = forms.BookForm(request.POST).save()

        context['books'] = models.Book.objects.all()

        context['feedback'] = '{0} added to {1} category!'.format(
                new_book.title, new_book.category.name)
        return render(request, 'book-create.html', context, status=201)

    return render(request, 'book-create.html', context)


def book_edit(request, book_id):
    book = models.Book.objects.get(pk=book_id)
    context = {
        'book_id': book_id,
        'book_form': forms.BookForm(initial={
            'category': book.category,
            'title': book.title
            })
    }
    if 'title' in request.POST or 'category' in request.POST:
        if request.POST.get('title') and book.title != request.POST['title']:
            book.title = request.POST['title']

        new_category = request.POST.get('category')
        if new_category and book.category != new_category:
            category = models.Category.objects.get(pk=new_category)
            book.category = category

        book.save()
        context['feedback'] = 'Edit successful!'

        return render(request, 'book-edit.html', context)
    return render(request, 'book-edit.html', context)

