from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.text import slugify

class User(AbstractUser):
    # любые кастомные поля
    pass

class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название отдела')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL-имя')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название должности')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL-имя')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='positions', verbose_name='Отдел')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['name']
        unique_together = ['name', 'department']

    def __str__(self):
        return f"{self.name} ({self.department.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees', verbose_name='Отдел')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='employees', verbose_name='Должность')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    bio = models.TextField(blank=True, verbose_name='О себе')
    skills = models.TextField(blank=True, verbose_name='Навыки')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    hire_date = models.DateField(null=True, blank=True, verbose_name='Дата приема на работу')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['user__last_name', 'user__first_name']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['department']),
            models.Index(fields=['position']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position.name if self.position else 'Без должности'}"

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email

    @property
    def department_name(self):
        return self.department.name if self.department else 'Не указан'

    @property
    def position_name(self):
        return self.position.name if self.position else 'Не указана'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('employees:employee_detail', kwargs={'pk': self.user.pk})