# Generated by Django 4.1.6 on 2023-03-29 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_student_limit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='reqDesc',
            new_name='bookAuthor',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='reqType',
            new_name='bookTitle',
        ),
        migrations.RemoveField(
            model_name='request',
            name='reqDate',
        ),
        migrations.AddField(
            model_name='request',
            name='bookEdition',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='bookLanguage',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
