# Generated by Django 4.2.7 on 2023-12-03 22:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Draw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draw_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Pairing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draw', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.draw')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('in_draw', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.draw')),
                ('in_pairing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.pairing')),
            ],
        ),
        migrations.AddField(
            model_name='pairing',
            name='participant_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='participants_1', to='app.participant'),
        ),
        migrations.AddField(
            model_name='pairing',
            name='participant_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='participants_2', to='app.participant'),
        ),
    ]
