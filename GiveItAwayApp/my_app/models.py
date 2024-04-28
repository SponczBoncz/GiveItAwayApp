from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

TYPE_CHOICES = [
    (0, 'fundacja'),
    (1, 'organizacja pozarządowa'),
    (2, 'zbiórka lokalna'),
]

class Category(models.Model):
    '''
    Attributes:
        name: CharField with max length of 64 characters. Should be unique.

    Methods:
        str: Returns the name of the category.
    '''

    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Institution(models.Model):
    '''
    Attributes:
        name: CharField with max length of 64 characters. Should be unique.
        description: TextField to provide additional information about the institution.
        type: IntegerField with choices defined in TYPE_CHOICES (fundacja, organizacja pozarządowa, zbiórka lokalna).
                Default value is 0 (fundacja).
        categories: Many-to-Many relationship with Category model.


    Methods:
        str: Returns the name of the category.
    '''

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES, default=0)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

class Donation(models.Model):

    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=64)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    is_taken = models.BooleanField(default=False)
