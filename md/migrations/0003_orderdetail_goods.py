# Generated by Django 2.1.4 on 2019-09-10 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('md', '0002_auto_20190907_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='goods',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
