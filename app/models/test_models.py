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
