# Generated by Django 4.2.20 on 2025-05-21 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA_project', '0007_alter_answer_edited_at_alter_question_edited_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default_avatar.jpeg', null=True, upload_to='avatars/'),
        ),
    ]
