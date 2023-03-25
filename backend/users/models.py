from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    USER_ROLES = (
        (USER, 'User'),
        (ADMIN, 'Admin'),
    )
    role = models.CharField(
        'Пользовательская роль',
        max_length=30,
        help_text='Администратор или обычный пользователь.'
        'По умолчанию `user`.',
        choices=USER_ROLES,
        default='user'
    )

    username = models.CharField('Имя пользователя', blank=True,
                                unique=True, max_length=128)
    email = models.EmailField('email address', blank=True, unique=True)
    first_name = models.CharField('Имя', blank=True, max_length=128)
    last_name = models.CharField('Фамилия', blank=True, max_length=128)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return f'{self.username}'


class Follow(models.Model):
    # Модель подписок
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    def save(self, **kwargs):
        if self.user == self.author:
            raise ValidationError("Невозможно подписаться на себя")
        super().save()

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-author_id']

    def __str__(self):
        return f'Автор: {self.author}, подписчик: {self.user}'
