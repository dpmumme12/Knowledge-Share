# Generated by Django 4.0.2 on 2022-03-08 04:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgebase', '0002_alter_article_author_alter_article_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
    ]
