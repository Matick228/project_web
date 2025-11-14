from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=_('Название категории'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Категория услуг')
        verbose_name_plural = _('Категории услуг')

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, verbose_name=_('Email почта'))
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Телефон'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=_('Название филиала'))
    address = models.CharField(max_length=255, verbose_name=_('Адрес'))
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Телефон'))
    work_hours = models.CharField(max_length=100, verbose_name=_('Часы работы'))
    photo = models.ImageField(upload_to='branches/', blank=True, null=True, verbose_name=_('Фото'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Филиал МФЦ')
        verbose_name_plural = _('Филиалы МФЦ')

class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name=_('Название статуса'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Статус заявки')
        verbose_name_plural = _('Статусы заявок')

class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name=_('Категория'))
    name = models.CharField(max_length=100, verbose_name=_('Название услуги'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Описание'))
    state_duty = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_('Госпошлина'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Услуга')
        verbose_name_plural = _('Услуги')

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, verbose_name=_('Услуга'))
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, verbose_name=_('Филиал'))
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, verbose_name=_('Статус'))
    desired_date = models.DateField(verbose_name=_('Желаемая дата'))
    desired_time = models.TimeField(verbose_name=_('Желаемое время'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    def __str__(self):
        return f"Запись #{self.appointment_id} - {self.user}"

    class Meta:
        verbose_name = _('Запись на приём')
        verbose_name_plural = _('Записи на приём')

class FavoriteService(models.Model):
    favorite_service_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь 123'))
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name=_('Услуга 1337'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата добавления вчера'))

    def __str__(self):
        return f"{self.user} -> {self.service}"

    class Meta:
        verbose_name = _('Избранная услуга')
        verbose_name_plural = _('Избранные услуги')
        constraints = [
            models.UniqueConstraint(fields=['user', 'service'], name='unique_user_service')
        ]


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class ServiceStatistic(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    view_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    appointment_count = models.IntegerField(default=0, verbose_name='Количество записей')

    def __str__(self):
        return f"Статистика: {self.service.name}"

    class Meta:
        verbose_name = 'Статистика услуги'
        verbose_name_plural = 'Статистика услуг'