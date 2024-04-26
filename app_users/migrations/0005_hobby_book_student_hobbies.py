# Generated by Django 5.0.4 on 2024-04-25 03:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0004_alter_student_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app_users.student')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='hobbies',
            field=models.ManyToManyField(to='app_users.hobby'),
        ),
    ]
