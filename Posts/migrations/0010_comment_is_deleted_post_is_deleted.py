# Generated by Django 4.1.6 on 2023-04-19 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0009_comment_password_post_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]