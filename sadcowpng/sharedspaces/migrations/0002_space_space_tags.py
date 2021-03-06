# Generated by Django 3.1.7 on 2021-04-29 04:57

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('sharedspaces', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='space_tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
