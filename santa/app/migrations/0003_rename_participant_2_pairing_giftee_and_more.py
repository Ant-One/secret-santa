# Generated by Django 4.2.7 on 2023-12-04 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_draw_is_drawn_participant_has_drawn_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pairing',
            old_name='participant_2',
            new_name='giftee',
        ),
        migrations.RenameField(
            model_name='pairing',
            old_name='participant_1',
            new_name='gifter',
        ),
        migrations.RenameField(
            model_name='participant',
            old_name='in_pairing',
            new_name='to_gift',
        ),
        migrations.AddField(
            model_name='participant',
            name='was_drawn',
            field=models.BooleanField(default=False),
        ),
    ]
