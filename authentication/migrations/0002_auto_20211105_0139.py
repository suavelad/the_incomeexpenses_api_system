# Generated by Django 3.2.9 on 2021-11-05 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='firstname',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='lastname',
            new_name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=255, null=True),
        ),
    ]
