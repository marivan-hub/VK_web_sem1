# Generated by Django 4.2.20 on 2025-04-09 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA_project', '0002_remove_answer_edited_at_remove_answerlike_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='description',
            field=models.CharField(default=''),
        ),
    ]
