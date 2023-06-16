from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name='название проекта')
    photo = models.ImageField(upload_to='project_photos/', verbose_name='фото проекта')
    description = models.TextField(verbose_name='описание проета')
    is_approved = models.BooleanField(default=False, verbose_name= 'отображение на сайте или нет')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'проект'
        verbose_name_plural = 'проекты'


class UserAppeal(models.Model):
    name = models.CharField(max_length=50, verbose_name='имя клиента')
    mail = models.EmailField(verbose_name='почта')
    message = models.TextField(verbose_name='заявка')
    date = models.DateField(auto_now_add=True, verbose_name='Дата заявки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'