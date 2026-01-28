import requests
from decimal import Decimal
from .models import Pool


class DefiLlamaService:
    """Fetches yield data from DeFiLlama API."""
    
    BASE_URL = "https://yields.llama.fi"
    
    def fetch_pools(self):
        """Fetch all pools from DeFiLlama."""
        
        print("Fetching pools from DeFiLlama...")
        response = requests.get(f"{self.BASE_URL}/pools")
        response.raise_for_status()
        
        data = response.json()
        pools = data.get("data", [])
        
        print(f"Found {len(pools)} pools")
        return pools
    
    def sync_pools(self, limit=100):
        """
        Fetch pools and save to database.
        
        Args:
            limit: Max pools to save (for testing)
        """
        
        raw_pools = self.fetch_pools()
        
        created = 0
        updated = 0
        skipped = 0
        
        for raw in raw_pools[:limit]:
            result = self._save_pool(raw)
            
            if result == "created":
                created += 1
            elif result == "updated":
                updated += 1
            else:
                skipped += 1
        
        print(f"Done! Created: {created}, Updated: {updated}, Skipped: {skipped}")
        
        return {"created": created, "updated": updated, "skipped": skipped}
    
    def _save_pool(self, raw):
        """Save a single pool to database."""
        
        pool_id = raw.get("pool")
        if not pool_id:
            return "skipped"
        
        # Skip pools with very low TVL
        tvl = raw.get("tvlUsd") or 0
        if tvl < 10000:
            return "skipped"
        
        # Prepare data
        defaults = {
            "protocol": raw.get("project", "unknown"),
            "chain": raw.get("chain", "unknown"),
            "symbol": raw.get("symbol", "unknown"),
            "apy": self._to_decimal(raw.get("apy")),
            "tvl": self._to_decimal(raw.get("tvlUsd")),
        }
        
        # Create or update
        pool, created = Pool.objects.update_or_create(
            pool_id=pool_id,
            defaults=defaults
        )
        
        return "created" if created else "updated"
    
    def _to_decimal(self, value):
        """Safely convert to Decimal."""
        if value is None:
            return None
        try:
            return Decimal(str(value))
        except:
            return None