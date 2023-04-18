# Generated by Django 4.1.6 on 2023-04-18 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50)),
                ('author_ip', models.CharField(max_length=15)),
                ('content', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Posts.post')),
            ],
        ),
    ]