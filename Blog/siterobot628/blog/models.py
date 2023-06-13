from django.db import models
from django.db.models.query import QuerySet
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    """Создаём свой менеджер моделей (objects)"""
    def get_queryset(self) -> QuerySet:
        quearyset = super().get_queryset()
        return quearyset.filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """Класс модель поста, которая хранит посты блога данных в бд"""
    
    class Status(models.TextChoices):
        """Класс для статуса блога"""

        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(
        max_length=250, 
        verbose_name='название',
        null=True,
        blank=True
    )
    
    slug = models.SlugField(
        max_length=250,
        verbose_name='метка',
        # предотвратит сохранение нового поста с тем же именем на дату публикации
        unique_for_date='publish',
        null=True,
        blank=True
    )
    
    author = models.ForeignKey(
        verbose_name='автор',
        to=User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )

    body = models.TextField(
        verbose_name='текст поста',
        null=True,
        blank=True
    )
    
    publish = models.DateTimeField(
        verbose_name='дата публикации',
        default=timezone.now
    )
    
    status = models.CharField(
        verbose_name='статус поста',
        max_length=2,
        choices=Status.choices,  # для получения всех статусов что есть
        default=Status.DRAFT
    )

    created = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True
    )
    
    updated = models.DateTimeField(
        verbose_name='дата обновления',
        auto_now=True
    )

    objects = models.Manager()  # менеджер по умолчанию
    published = PublishedManager()  # кастомный менеджер

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail', 
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'post'
        ordering = ['-publish']  # сортируется от новых к старым (обратный порядок)
        # индексирование повысит производительность запросов
        indexes = [
            models.Index(fields=['-publish'])
        ]
