# Generated by Django 4.0.1 on 2022-05-04 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_session_weight_blank_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='blank_num',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='correct_num',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='votation',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='exam',
            name='wrong_num',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
