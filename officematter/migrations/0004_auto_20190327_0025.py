# Generated by Django 2.1.7 on 2019-03-26 17:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('officematter', '0003_auto_20190317_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Achievement', models.ImageField(upload_to='images/')),
                ('Success', models.BooleanField()),
                ('Date', models.DateField()),
                ('ClientId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Achievement',
            },
        ),
        migrations.CreateModel(
            name='Contents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=500, unique=True)),
                ('Type', models.IntegerField()),
                ('Manager', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Organization',
            },
        ),
        migrations.CreateModel(
            name='OrganizationMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ClientId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('OrgId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='officematter.Organization')),
            ],
            options={
                'db_table': 'OrganizationMember',
            },
        ),
        migrations.AddField(
            model_name='achievement',
            name='OrgId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='officematter.Organization'),
        ),
    ]