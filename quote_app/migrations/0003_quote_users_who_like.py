# Generated by Django 2.2 on 2020-11-09 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote_app', '0002_quote_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='users_who_like',
            field=models.ManyToManyField(related_name='liked_quotes', to='quote_app.User'),
        ),
    ]
