from django.db import models


class Book(models.Model):
    BOOK_TYPES = (
        (1, 'Hardcover'),
        (2, 'Paperback'),
        (3, 'E-book'),
    )

    title = models.CharField(max_length=50)
    publication_date = models.DateField(null=True)
    author = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pages = models.IntegerField(blank=True, null=True)
    book_type = models.PositiveSmallIntegerField(choices=BOOK_TYPES)

    timestamp = models.DateField(auto_now_add=True, auto_now=False)
