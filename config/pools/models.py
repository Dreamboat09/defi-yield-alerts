from django.db import models

# Create your models here.

class Pool(models.Model):
    
    # Unique identifier from DeFiLlama
    pool_id = models.CharField(max_length=255, unique=True)
    
    # Basic info
    protocol = models.CharField(max_length=100)  # e.g., "aave-v3"
    chain = models.CharField(max_length=50)      # e.g., "ethereum"
    symbol = models.CharField(max_length=100)    # e.g., "USDC"
    
    # Yield data
    apy = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tvl = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.protocol} - {self.symbol} ({self.chain})"