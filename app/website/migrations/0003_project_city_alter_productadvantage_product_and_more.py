# Generated by Django 5.0 on 2024-01-04 16:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_color_project_colors'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='city',
            field=models.CharField(default='Tehran', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productadvantage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advantages', to='website.product'),
        ),
        migrations.AlterField(
            model_name='productdisadvantage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disadvantages', to='website.product'),
        ),
    ]