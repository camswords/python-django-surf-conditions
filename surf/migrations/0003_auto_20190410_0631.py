# Generated by Django 2.2 on 2019-04-10 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surf', '0002_auto_20190410_0608'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='surfreport',
            index=models.Index(fields=['-captured_at'], name='surf_surfre_capture_d78c70_idx'),
        ),
    ]