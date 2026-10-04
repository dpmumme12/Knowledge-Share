from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgebase', '0011_alter_article_user_folder'),
    ]

    operations = [
        TrigramExtension(),
    ]
