from rest_framework import serializers
from .models import Produk, Kategori, Status

class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class ProdukSerializer(serializers.ModelSerializer):
    nama_kategori = serializers.CharField(source='kategori.nama_kategori', read_only=True)
    nama_status = serializers.CharField(source='status.nama_status', read_only=True)
    
    kategori_id = serializers.PrimaryKeyRelatedField(
        queryset=Kategori.objects.all(), source='kategori', write_only=True
    )
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(), source='status', write_only=True
    )

    class Meta:
        model = Produk
        fields = [
            'id', 'nama_produk', 'harga', 
            'kategori_id', 'nama_kategori', 
            'status_id', 'nama_status'
        ]
