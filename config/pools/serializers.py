from rest_framework import serializers
from .models import Pool


class PoolSerializer(serializers.ModelSerializer):
    """Converts Pool model to JSON."""
    
    class Meta:
        model = Pool
        fields = [
            'pool_id',
            'protocol',
            'chain',
            'symbol',
            'apy',
            'tvl',
            'created_at',
            'updated_at',
        ]