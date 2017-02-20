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

