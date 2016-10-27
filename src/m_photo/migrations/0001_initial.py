# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 13:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('m_comment', '0001_initial'),
        ('m_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, editable=False, null=True, verbose_name='Deleted at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('last_edited_at', models.DateTimeField(auto_now=True, verbose_name='Last edited at')),
                ('like_count', models.PositiveIntegerField(default=0, editable=False, verbose_name='Like count')),
                ('dislike_count', models.PositiveIntegerField(default=0, editable=False, verbose_name='Dislike count')),
                ('rating', models.IntegerField(default=0, editable=False, verbose_name='Rating')),
                ('comment_count', models.PositiveIntegerField(default=0, editable=False, verbose_name='Comment count')),
                ('last_commented_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Last commented at')),
                ('image', models.ImageField(height_field='height', upload_to=b'', verbose_name='Image file', width_field='width')),
                ('height', models.PositiveIntegerField(verbose_name='Image height')),
                ('width', models.PositiveIntegerField(verbose_name='Image width')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhotoAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Is deleted')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, editable=False, null=True, verbose_name='Deleted at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('last_edited_at', models.DateTimeField(auto_now=True, verbose_name='Last edited at')),
                ('like_count', models.PositiveIntegerField(default=0, editable=False, verbose_name='Like count')),
                ('dislike_count', models.PositiveIntegerField(default=0, editable=False, verbose_name='Dislike count')),
                ('rating', models.IntegerField(default=0, editable=False, verbose_name='Rating')),
                ('comment_count', models.PositiveIntegerField(default=0, editable=False, verbose_name='Comment count')),
                ('last_commented_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Last commented at')),
                ('name', models.CharField(max_length=256, verbose_name='Album name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('last_comment', models.ForeignKey(blank=True, db_index=False, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_comment+', to='m_comment.Comment', verbose_name='Last comment')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='album', to='m_profile.Profile', verbose_name='Album owner')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='photo',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo', to='m_photo.PhotoAlbum', verbose_name='Album'),
        ),
        migrations.AddField(
            model_name='photo',
            name='last_comment',
            field=models.ForeignKey(blank=True, db_index=False, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_comment+', to='m_comment.Comment', verbose_name='Last comment'),
        ),
    ]
