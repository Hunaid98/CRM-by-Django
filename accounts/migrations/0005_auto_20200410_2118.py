# Generated by Django 2.2.12 on 2020-04-10 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200410_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='Tags',
        ),
        migrations.AddField(
            model_name='products',
            name='Tags',
            field=models.ManyToManyField(to='accounts.Tag'),
        ),
    ]
