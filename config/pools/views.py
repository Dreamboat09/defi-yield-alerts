from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Pool
from .serializers import PoolSerializer
from .services import DefiLlamaService


@api_view(['GET'])
def pool_list(request):
    """
    Get all pools.
    
    Optional filters:
    - chain: filter by chain (e.g., ?chain=ethereum)
    - min_apy: minimum APY (e.g., ?min_apy=5)
    - min_tvl: minimum TVL (e.g., ?min_tvl=1000000)
    """
    
    pools = Pool.objects.all()
    
    # Filter by chain
    chain = request.query_params.get('chain')
    if chain:
        pools = pools.filter(chain=chain.lower())
    
    # Filter by minimum APY
    min_apy = request.query_params.get('min_apy')
    if min_apy:
        pools = pools.filter(apy__gte=min_apy)
    
    # Filter by minimum TVL
    min_tvl = request.query_params.get('min_tvl')
    if min_tvl:
        pools = pools.filter(tvl__gte=min_tvl)
    
    # Order by APY descending
    pools = pools.order_by('-apy')[:100]
    
    serializer = PoolSerializer(pools, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def pool_detail(request, pool_id):
    """Get a single pool by ID."""
    
    try:
        pool = Pool.objects.get(pool_id=pool_id)
    except Pool.DoesNotExist:
        return Response(
            {'error': 'Pool not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = PoolSerializer(pool)
    return Response(serializer.data)


@api_view(['POST'])
def sync_pools(request):
    """Fetch latest data from DeFiLlama."""
    
    limit = request.data.get('limit', 100)
    
    service = DefiLlamaService()
    result = service.sync_pools(limit=limit)
    
    return Response({
        'message': 'Sync complete',
        'result': result
    })