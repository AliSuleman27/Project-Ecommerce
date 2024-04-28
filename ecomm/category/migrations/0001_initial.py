# Generated by Django 5.0.4 on 2024-04-26 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('categorey_image', models.ImageField(blank=True, null=True, upload_to='categories')),
            ],
        ),
    ]
