from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    # Тэги
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        db_index=True,
        unique=True
    )
    hexcolor = models.CharField(
        max_length=7,
        default="#ffffff",
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    measurement_unit = models.CharField(max_length=10, verbose_name='Единицы измерения')

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    # Модель рецептов
    RECIPE_NUM: int = 10

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.TextField(
        verbose_name='Название рецепта',
        help_text='Название рецепта'
    )
    text = models.TextField(
        verbose_name='Описание'
    )

    image = models.ImageField(
        'Картинка',
        upload_to='recipes/'
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='продукт'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tag',
        verbose_name='тэг'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(MinValueValidator(
            limit_value=1,
            message='Время приготовления не может быть менее одной минуты.'),
        )
    )

    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        # выводим текст поста
        return self.name[0:30]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipes'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(MinValueValidator(
            limit_value=0.01,
            message='Количество должно быть больше нуля'),
        )
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return (f'{self.recipe}: {self.ingredient.name},'
                f' {self.amount}, {self.ingredient.measurement_unit}')


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепты',
        related_name='favorite'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепты',
        related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'

    def __str__(self):
        return f'{self.recipe} в корзине у {self.user}'