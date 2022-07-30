# Generated by Django 3.1.5 on 2021-08-14 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('purchase_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('method', models.CharField(max_length=255)),
                ('coins', models.IntegerField()),
                ('money', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name': 'Purchase',
                'verbose_name_plural': 'Purchase',
            },
        ),
    ]
