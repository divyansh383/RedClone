# Generated by Django 4.1.2 on 2023-02-16 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_likedpost'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='likedpost',
            unique_together={('liked_by', 'liked_post')},
        ),
    ]
