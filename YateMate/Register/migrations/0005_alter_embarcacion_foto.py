# Generated by Django 5.0.4 on 2024-05-30 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Register', '0004_user_moroso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='embarcacion',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='static/img_b'),
        ),
    ]
