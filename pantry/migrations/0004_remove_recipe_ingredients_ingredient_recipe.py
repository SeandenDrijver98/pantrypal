# Generated by Django 4.2 on 2024-08-04 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pantry', '0003_foodinventory_remove_nutrientvalue_food_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='pantry.recipe'),
            preserve_default=False,
        ),
    ]
