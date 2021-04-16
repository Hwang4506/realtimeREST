from rest_framework import serializers
from .models import Realbar

class BarcodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Realbar
        fields = ['id', 'barcode', 'create_date']