# Generated manually to fix unsubscribed_at field
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("miscellaneous", "0011_alter_subscriber_confirmation_code_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscriber",
            name="unsubscribed_at",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Date de désouscription"
            ),
        ),
    ]
