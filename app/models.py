from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Artikel(models.Model):
    idartikel = models.AutoField(primary_key=True)
    kategori = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    description = models.TextField()
    date = models.DateField()
    img = models.ImageField()

    def __str__(self):
        return self.title
    
class Banner(models.Model):
    idbanner = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 255)
    img = models.ImageField()
    
class Profesional(models.Model):
    CHOICES = (
        ('TA', 'Temu Arsitek'),
        ('TK', 'Temu Kontraktor'),
    )
    idprof = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    no_telp_pemesan = models.IntegerField()
    tanggal_ketemu = models.DateTimeField()
    layanan = models.CharField(max_length=300, choices = CHOICES)
    nama_penerima = models.CharField(max_length = 200, null=True)
    no_telp_penerima = models.IntegerField(null=True)

class Worker(models.Model):
    CHOICES = (
        ('PB', 'Pekerja Bangunan'),
        ('PA', 'Pekerja AC'),
    )
    idworker = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    no_telp_pemesan = models.IntegerField()
    tanggal_ketemu = models.DateTimeField()
    layanan = models.CharField(max_length=300, choices = CHOICES)
    nama_penerima = models.CharField(max_length = 200, null=True)
    no_telp_penerima = models.IntegerField(null=True)

class Items(models.Model):
    iditems = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    no_telp_pemesan = models.IntegerField()
    tanggal_ketemu = models.DateTimeField()
    layanan = models.CharField(max_length=300)
    jumlah = models.IntegerField()
    nama_penerima = models.CharField(max_length = 200, null=True)
    alamat = models.CharField(max_length = 255, null=True)
    no_telp_penerima = models.IntegerField(null=True)