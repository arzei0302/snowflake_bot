# Generated by Django 3.2.7 on 2023-06-13 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(verbose_name='описание проета'),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='отображение на сайте или нет'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=255, verbose_name='название проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='photo',
            field=models.ImageField(upload_to='project_photos/', verbose_name='фото проекта'),
        ),
    ]