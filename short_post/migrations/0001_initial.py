# Generated by Django 2.2.1 on 2020-02-29 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostContent',
            fields=[
                ('post_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=172, verbose_name='投稿内容')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'post_content',
                'verbose_name_plural': 'post_contents',
                'db_table': 'post_content',
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('follow_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('follow_user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='follow_user', to=settings.AUTH_USER_MODEL)),
                ('followed_user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='followed_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'follow',
                'verbose_name_plural': 'followes',
                'db_table': 'follow',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('favorite_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('post_content', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='short_post.PostContent')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'favorite',
                'verbose_name_plural': 'favorites',
                'db_table': 'favorite',
            },
        ),
    ]