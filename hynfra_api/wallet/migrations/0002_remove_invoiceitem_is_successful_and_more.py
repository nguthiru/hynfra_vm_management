# Generated by Django 5.1.1 on 2024-09-08 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceitem',
            name='is_successful',
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('billing_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallet.billingprofile')),
                ('items', models.ManyToManyField(to='wallet.invoiceitem')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
