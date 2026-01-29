from decimal import Decimal
from pools.models import Pool
from .models import AlertRule, AlertHistory


class AlertEngine:
    """Evaluates alert rules against pool data."""
    
    def check_all_rules(self):
        """Check all active rules against all pools."""
        
        rules = AlertRule.objects.filter(is_active=True)
        pools = Pool.objects.all()
        
        print(f"Checking {rules.count()} rules against {pools.count()} pools...")
        
        alerts_triggered = []
        
        for rule in rules:
            triggered = self._check_rule(rule, pools)
            alerts_triggered.extend(triggered)
        
        print(f"Triggered {len(alerts_triggered)} alerts")
        return alerts_triggered
    
    def _check_rule(self, rule, pools):
        """Check a single rule against pools."""
        
        triggered = []
        
        # Filter pools by rule's chain/protocol if specified
        filtered_pools = pools
        
        if rule.chain:
            filtered_pools = filtered_pools.filter(chain=rule.chain.lower())
        
        if rule.protocol:
            filtered_pools = filtered_pools.filter(protocol=rule.protocol.lower())
        
        for pool in filtered_pools:
            result = self._evaluate_condition(rule, pool)
            
            if result:
                alert = self._create_alert(rule, pool, result)
                triggered.append(alert)
        
        return triggered
    
    def _evaluate_condition(self, rule, pool):
        """Check if a pool meets the rule's condition."""
        
        # Get the value to check
        if rule.rule_type in [AlertRule.TYPE_APY_ABOVE, AlertRule.TYPE_APY_BELOW]:
            value = pool.apy
        else:
            value = pool.tvl
        
        if value is None:
            return None
        
        # Check condition
        threshold = rule.threshold
        
        if rule.rule_type == AlertRule.TYPE_APY_ABOVE:
            if value > threshold:
                return {'value': value, 'condition': 'above', 'field': 'APY'}
        
        elif rule.rule_type == AlertRule.TYPE_APY_BELOW:
            if value < threshold:
                return {'value': value, 'condition': 'below', 'field': 'APY'}
        
        elif rule.rule_type == AlertRule.TYPE_TVL_ABOVE:
            if value > threshold:
                return {'value': value, 'condition': 'above', 'field': 'TVL'}
        
        elif rule.rule_type == AlertRule.TYPE_TVL_BELOW:
            if value < threshold:
                return {'value': value, 'condition': 'below', 'field': 'TVL'}
        
        return None
    
    def _create_alert(self, rule, pool, result):
        """Create an alert history record."""
        
        message = (
            f"{pool.protocol} - {pool.symbol} on {pool.chain}: "
            f"{result['field']} is {result['value']:.2f}, "
            f"which is {result['condition']} your threshold of {rule.threshold}"
        )
        
        alert = AlertHistory.objects.create(
            rule=rule,
            pool_id=pool.pool_id,
            pool_symbol=pool.symbol,
            pool_protocol=pool.protocol,
            triggered_value=result['value'],
            message=message
        )
        
        print(f"ALERT: {message}")
        return alert