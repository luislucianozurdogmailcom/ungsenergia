# Generated by Django 3.1.5 on 2022-05-10 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_usuario', models.IntegerField()),
                ('usuario', models.CharField(max_length=60)),
                ('contraseña', models.CharField(max_length=60)),
                ('mail', models.CharField(max_length=60)),
                ('nombre', models.CharField(max_length=60)),
                ('apellido', models.CharField(max_length=60)),
                ('celular', models.CharField(max_length=60)),
            ],
        ),
    ]
