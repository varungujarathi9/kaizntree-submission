# Generated by Django 5.0.2 on 2024-02-12 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kaizntree_app', '0002_rename_item_id_item_id_item_created_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=models.CharField(choices=[('ET', 'Etsy'), ('CT', 'In Shop'), ('ST', 'Settings'), ('OL', 'Online'), ('SP', 'Shopify'), ('SQ', 'Square'), ('XE', 'Xero')], max_length=100),
        ),
    ]
