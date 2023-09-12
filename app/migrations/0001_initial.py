# Generated by Django 4.1.4 on 2023-09-11 04:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('idbanner', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=255)),
                ('img', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('idworker', models.AutoField(primary_key=True, serialize=False)),
                ('no_telp_pemesan', models.IntegerField()),
                ('tanggal_ketemu', models.DateTimeField()),
                ('layanan', models.CharField(choices=[('PB', 'Pekerja Bangunan'), ('PA', 'Pekerja AC')], max_length=300)),
                ('nama_penerima', models.CharField(max_length=200, null=True)),
                ('no_telp_penerima', models.IntegerField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profesional',
            fields=[
                ('idprof', models.AutoField(primary_key=True, serialize=False)),
                ('no_telp_pemesan', models.IntegerField()),
                ('tanggal_ketemu', models.DateTimeField()),
                ('layanan', models.CharField(choices=[('TA', 'Temu Arsitek'), ('TK', 'Temu Kontraktor')], max_length=300)),
                ('nama_penerima', models.CharField(max_length=200, null=True)),
                ('no_telp_penerima', models.IntegerField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('iditems', models.AutoField(primary_key=True, serialize=False)),
                ('no_telp_pemesan', models.IntegerField()),
                ('tanggal_ketemu', models.DateTimeField()),
                ('layanan', models.CharField(max_length=300)),
                ('jumlah', models.IntegerField()),
                ('nama_penerima', models.CharField(max_length=200, null=True)),
                ('alamat', models.CharField(max_length=255, null=True)),
                ('no_telp_penerima', models.IntegerField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Artikel',
            fields=[
                ('idartikel', models.AutoField(primary_key=True, serialize=False)),
                ('kategori', models.CharField(max_length=300)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('img', models.ImageField(upload_to='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]