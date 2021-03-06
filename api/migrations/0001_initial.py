# Generated by Django 4.0 on 2021-12-22 21:50

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('balance', models.IntegerField()),
                ('pin', models.CharField(max_length=6)),
                ('active', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('telephone', models.CharField(blank=True, max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('nid', models.CharField(max_length=14, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=20)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('payment', models.CharField(choices=[('made', 'made'), ('missed', 'missed')], default='missed', max_length=6)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.loan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='account',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.client'),
        ),
    ]
