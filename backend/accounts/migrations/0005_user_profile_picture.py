# Generated by Django 4.1.2 on 2022-12-26 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_folowers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='profiles'),
        ),
    ]
