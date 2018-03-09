# Generated by Django 2.0.2 on 2018-03-09 20:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permissions', models.TextField()),
                ('value', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DeployJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('completed_at', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('failed', 'failed'), ('finished', 'finished')], default='pending', max_length=255)),
                ('image_tag', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('login', models.CharField(max_length=255)),
                ('host', models.CharField(max_length=255)),
                ('port', models.PositiveIntegerField()),
                ('is_provisioned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='NodeProvisionJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('completed_at', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('failed', 'failed'), ('finished', 'finished')], default='pending', max_length=255)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='snailshell_cp.Node')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=255)),
                ('default_image_tag', models.CharField(max_length=255)),
                ('container_name', models.CharField(max_length=255)),
                ('is_system_service', models.BooleanField(default=False)),
                ('env_variables', models.TextField(blank=True, help_text='JSON, containing a key: value map. If value starts with $ - it is considered to be a name settings variable, the value will be sent over', null=True)),
                ('host_config', models.TextField(blank=True, help_text='JSON to be passed to container creation Docker API endpoint', null=True)),
                ('volumes', models.TextField(blank=True, help_text='JSON to be passed to container creation Docker API endpoint', null=True)),
                ('command', models.TextField(help_text='JSON, passed to `Cmd` parameter on container creation')),
                ('user_name', models.CharField(blank=True, help_text='Linux user to run the container with', max_length=255, null=True)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='snailshell_cp.Node')),
            ],
        ),
        migrations.AddField(
            model_name='deployjob',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='snailshell_cp.Service'),
        ),
    ]
