# Generated by Django 3.2.12 on 2022-04-04 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_comment_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='likes',
        ),
        migrations.AddField(
            model_name='food',
            name='likes',
            field=models.ManyToManyField(related_name='user_likes', to='accounts.User'),
        ),
    ]
