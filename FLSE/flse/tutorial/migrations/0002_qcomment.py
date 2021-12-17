# Generated by Django 2.2.13 on 2020-10-07 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tutorial', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qcomment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.IntegerField(default=0)),
                ('r_token', models.BooleanField(default=False)),
                ('date_published', models.DateTimeField(default=django.utils.timezone.now)),
                ('qcomment', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Qcomments', to='tutorial.Comment')),
                ('liked_by', models.ManyToManyField(blank=True, related_name='liked_by_qcomment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
