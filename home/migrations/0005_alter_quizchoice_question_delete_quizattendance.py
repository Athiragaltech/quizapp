# Generated by Django 5.0.3 on 2024-04-17 06:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_user_quiz_quizquestion_quizchoice_quizattendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizchoice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='home.quizquestion'),
        ),
        migrations.DeleteModel(
            name='QuizAttendance',
        ),
    ]
