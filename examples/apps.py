import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Set

from django.apps import AppConfig


@dataclass(frozen=True)
class ExampleBook:
    title: str
    publication_date: datetime
    author: str
    price: float
    pages: int
    book_type: int  # REMEMBER: 1 = 'Hardcover', 2 = 'Paperback', 3 = 'E-book'


def get_example_books() -> Set[ExampleBook]:
    return {
        ExampleBook('Lord of the Rings - 3-Book Paperback Box Set', datetime(year=1954, month=7, day=29), 'J.R.R. Tolkien', 19.99, 1536, 2),
        ExampleBook('Lord of the Flies - Large Print Edition', datetime(year=1954, month=9, day=17), 'William Golding', 25.95, 286, 2),
    }


class ExamplesConfig(AppConfig):
    name = 'examples'

    def ready(self) -> None:
        # ATTENTION: Leave the imports here!!!
        from examples.models import Book
        # Pushing during any migration operation, is not that clever...
        if not any(arg in ('makemigrations', 'migrate') for arg in sys.argv):
            # Push some examples to play around, if DB is empty...
            if Book.objects.all().count() < 1:
                books = [Book(title=book.title, publication_date=book.publication_date, author=book.author, price=book.price, pages=book.pages, book_type=book.book_type) for book in get_example_books()]
                Book.objects.bulk_create(books)
