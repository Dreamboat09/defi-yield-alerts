from django.db import models

# Create your models here.

class AlertRule(models.Model):
    """A rule that triggers alerts when conditions are met."""
    
    # Rule types
    TYPE_APY_ABOVE = 'apy_above'
    TYPE_APY_BELOW = 'apy_below'
    TYPE_TVL_ABOVE = 'tvl_above'
    TYPE_TVL_BELOW = 'tvl_below'
    
    TYPE_CHOICES = [
        (TYPE_APY_ABOVE, 'APY goes above'),
        (TYPE_APY_BELOW, 'APY goes below'),
        (TYPE_TVL_ABOVE, 'TVL goes above'),
        (TYPE_TVL_BELOW, 'TVL goes below'),
    ]
    
    # Rule definition
    name = models.CharField(max_length=100)
    rule_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    threshold = models.DecimalField(max_digits=20, decimal_places=2)
    
    # Optional filters
    chain = models.CharField(max_length=50, blank=True)
    protocol = models.CharField(max_length=100, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_rule_type_display()} {self.threshold})"


class AlertHistory(models.Model):
    """Record of triggered alerts."""
    
    rule = models.ForeignKey(AlertRule, on_delete=models.CASCADE, related_name='history')
    pool_id = models.CharField(max_length=255)
    pool_symbol = models.CharField(max_length=100)
    pool_protocol = models.CharField(max_length=100)
    
    # Value that triggered the alert
    triggered_value = models.DecimalField(max_digits=20, decimal_places=2)
    message = models.TextField()
    
    # Timestamp
    triggered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rule.name} - {self.pool_symbol} at {self.triggered_at}"

    class Meta:
        verbose_name_plural = "Alert histories"