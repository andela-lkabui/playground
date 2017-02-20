from django.db import models

# Create your models here.


class Category(models.Model):
    """
    The model for book Categories.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        """Customizes the string representation of the Category model."""
        return '{0}'.format(self.name)