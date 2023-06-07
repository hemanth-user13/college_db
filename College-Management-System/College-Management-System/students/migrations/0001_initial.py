# Generated by Django 4.2.1 on 2023-05-23 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentClassInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=20)),
                ('class_short_form', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='StudentSectionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='StudentShiftInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_year', models.CharField(max_length=100)),
                ('admission_date', models.DateField()),
                ('admission_id', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('student_img', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('fathers_name', models.CharField(max_length=100)),
                ('fathers_img', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('fathers_nid', models.IntegerField(unique=True)),
                ('fathers_number', models.IntegerField(unique=True)),
                ('mothers_name', models.CharField(max_length=100)),
                ('mothers_img', models.ImageField(upload_to='photos/%Y/%m/%d/')),
                ('mothers_nid', models.IntegerField(unique=True)),
                ('mothers_number', models.IntegerField()),
                ('class_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.studentclassinfo')),
                ('section_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.studentsectioninfo')),
                ('shift_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.studentshiftinfo')),
            ],
            options={
                'unique_together': {('admission_id', 'class_type')},
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.IntegerField(default=0)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.studentinfo')),
            ],
            options={
                'unique_together': {('student', 'date')},
            },
        ),
    ]
