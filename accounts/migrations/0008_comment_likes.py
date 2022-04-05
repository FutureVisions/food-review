# Generated by Django 3.2.12 on 2022-04-04 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_comment_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(related_name='food_likes', to='accounts.Food'),
        ),
    ]
