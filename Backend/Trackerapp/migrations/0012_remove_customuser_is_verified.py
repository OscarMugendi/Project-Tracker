from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Trackerapp', '0011_merge_0008_auto_20211017_2325_0010_auto_20211019_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_verified',
        ),
    ]
