# Generated by Django 5.1.3 on 2024-12-13 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_noticeboard_bfile_thumbnail_noticeboard_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noticeboard',
            name='like_members',
        ),
        migrations.AddField(
            model_name='noticeboard',
            name='bmail',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
