# Generated by Django 5.1.3 on 2024-12-16 10:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin1', '0001_initial'),
        ('loginpage', '0002_member_created_group_member_joined_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoticeBoard',
            fields=[
                ('bno', models.AutoField(primary_key=True, serialize=False)),
                ('btitle', models.CharField(max_length=1000)),
                ('bcontent', models.TextField()),
                ('bdate', models.DateTimeField(auto_now=True)),
                ('bfile', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('bfile_thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('category', models.IntegerField(null=True)),
                ('like_members', models.ManyToManyField(blank=True, related_name='like_postboards', to='loginpage.member')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin1.administrator')),
            ],
        ),
    ]
