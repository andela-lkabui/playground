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

