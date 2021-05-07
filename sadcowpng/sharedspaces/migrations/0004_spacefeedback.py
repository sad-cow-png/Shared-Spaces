# Generated by Django 3.1.7 on 2021-05-04 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sharedspaces', '0003_auto_20210501_0345'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpaceFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('space_feedback', models.CharField(max_length=1000)),
                ('space_dt_reserved_by', models.CharField(default='No User', max_length=1000)),
                ('space_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='sharedspaces.space')),
            ],
        ),
    ]
