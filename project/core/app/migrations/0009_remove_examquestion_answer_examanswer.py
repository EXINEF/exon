# Generated by Django 4.0.4 on 2022-05-15 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_question_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examquestion',
            name='answer',
        ),
        migrations.CreateModel(
            name='ExamAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, null=True)),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.answer')),
                ('exam_question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.examquestion')),
            ],
        ),
    ]
