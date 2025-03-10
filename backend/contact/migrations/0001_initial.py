# Generated by Django 5.1.4 on 2025-02-20 20:25

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                (
                    "last_name",
                    models.CharField(max_length=100, verbose_name="Last Name"),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="Email Address"),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None, verbose_name="Phone Number"
                    ),
                ),
                ("message", models.TextField(verbose_name="Message")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Submitted At"
                    ),
                ),
            ],
            options={
                "verbose_name": "Contact",
                "verbose_name_plural": "Contacts",
                "ordering": ["-created_at"],
            },
        ),
    ]
