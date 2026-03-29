# Generated migration to fix NULL cookie_balance values

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_cookie_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cookie_balance',
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.RunPython(
            lambda apps, schema_editor: apps.get_model('users', 'User').objects.filter(cookie_balance__isnull=True).update(cookie_balance=100)
        ),
    ]
