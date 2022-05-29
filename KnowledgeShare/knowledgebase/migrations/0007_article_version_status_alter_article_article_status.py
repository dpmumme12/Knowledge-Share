# Generated by Django 4.0.2 on 2022-04-14 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgebase', '0006_folder_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='version_status',
            field=models.SmallIntegerField(choices=[(1, 'Active'), (2, 'History'), (3, 'New Version')], default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='article_status',
            field=models.SmallIntegerField(choices=[(1, 'Draft'), (2, 'Published'), (3, 'Archived')]),
        ),
    ]