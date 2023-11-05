from django.db import models
from django.urls import reverse


# менеджер записей возвразает опубликованные статьи
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    # вместо is_published 1 и 0 создали перечисление
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255)
    # используется хитрость миграции
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT,
                            related_name='posts')  # PROTECT - запрещает удаление категории
    tags = models.ManyToManyField('TagPost', blank=True,
                                  related_name='tags')  # related_name - атрибут связывает с катег
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   related_name='woman')  # SET_NULL - удаляет связи один к одному

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    # сортировка
    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    # возвращает юрл со слагом
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    # юрл отображается слаг
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

        # юрл отображается слаг

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name
