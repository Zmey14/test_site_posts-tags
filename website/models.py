from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Название вакансии')
    slug = models.SlugField(max_length=150, blank=True, unique=True, verbose_name='url')
    body = models.TextField(blank=True, db_index=True, verbose_name='Описание')
    # ManyToManyField создаётся в основном классе, и связывает его с указанным в модуле tags('Tag') классом
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    # auto_now_add - будет заполняться при сохранении в базу данных
    date_pub = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Вакансии'
        verbose_name = 'Вакансии'
        ordering = ['-date_pub']


class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название тэга')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='url')

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name_plural = 'Тэги'
        verbose_name = 'Тэг'
        ordering = ['title']
