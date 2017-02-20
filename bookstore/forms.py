from django.forms import ModelForm

from bookstore import models


class CategoryForm(ModelForm):
    """
    The form that is used for creating book Categories.
    """

    class Meta:
        model = models.Category
        fields = ['name']