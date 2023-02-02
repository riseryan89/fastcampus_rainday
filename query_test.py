from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Authors"


class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Books"


class AuthorMany(models.Model):
    name = models.CharField(max_length=100)


class BookMany(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(AuthorMany)



# generate_mock_data()
authors = Author.objects.prefetch_related("book_set")
for author in authors:
    books = author.book_set.all()
    print(f"Author: {author.name}, Books: {[book.title for book in books]}")

print("==" * 50)

books = Book.objects.select_related("author")
for book in books:
    author = book.author
    print(f"Book: {book.title}, Author: {author.name}")
print("==" * 50)

from django.db.models import Count

authors = Author.objects.annotate(book_count=Count("book"))
for author in authors:
    print(f"Author: {author.name}, Book count: {author.book_count}")
print("==" * 50)

books = Book.objects.annotate(author_count=Count("author"))
for book in books:
    print(f"Book: {book.title}, Author count: {book.author_count}")

print("==" * 50)

author = AuthorMany.objects.last()
books = author.bookmany_set.all()

for book in books:
    print(f"Book: {book.title}, Author: {book.authors.name}")

book = BookMany.objects.last()
authors = book.authors.all()
for author in authors:
    print(f"Author: {author.name}, Book: {author.bookmany_set.all()}")



def generate_mock_data(num_authors=5, num_books=10):
    import random
    from faker import Faker

    fake = Faker()

    for _ in range(num_authors):
        Author.objects.create(name=fake.name())

    authors = Author.objects.all()
    for _ in range(num_books):
        title = fake.sentence(nb_words=4)
        author = random.choice(authors)
        Book.objects.create(title=title, author=author)

    for _ in range(num_authors):
        AuthorMany.objects.create(name=fake.name())

    for _ in range(num_books * 2):
        title = fake.sentence(nb_words=4)
        authors = random.choice(AuthorMany.objects.all())
        book = BookMany.objects.create(title=title)
        book.authors.add(authors)
