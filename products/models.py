from django.db import models

class Kategori(models.Model):
    id = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'kategori'

    def __str__(self):
        return self.nama_kategori

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    nama_status = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'status'

    def __str__(self):
        return self.nama_status

class Produk(models.Model):
    id = models.AutoField(primary_key=True)
    nama_produk = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=12, decimal_places=0)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta:
        db_table = 'produk'

    def __str__(self):
        return self.nama_produk
