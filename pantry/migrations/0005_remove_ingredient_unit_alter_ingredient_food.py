# Generated by Django 4.2 on 2024-08-04 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pantry', '0004_remove_recipe_ingredients_ingredient_recipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='unit',
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pantry.food'),
        ),
    ]
