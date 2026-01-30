from django import forms
from .models import Produk

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['nama_produk', 'harga', 'kategori', 'status']
        widgets = {
            'nama_produk': forms.TextInput(attrs={'class': 'form-control'}),
            'harga': forms.NumberInput(attrs={'class': 'form-control'}),
            'kategori': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_harga(self):
        harga = self.cleaned_data.get('harga')
        if harga is None:
            raise forms.ValidationError("Harga is required")
        try:
            int(harga)
        except ValueError:
            raise forms.ValidationError("Harga must be numeric")
        return harga
