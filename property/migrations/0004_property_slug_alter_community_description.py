# Generated by Django 5.1.2 on 2025-01-11 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("property", "0003_community_agent_community_description_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="slug",
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="community",
            name="description",
            field=models.TextField(blank=True, default="No description", null=True),
        ),
    ]
