from rest_framework import viewsets
from rest_framework.response import Response

from .models import Colors, Product
#
from .serializers import (
    ColorsSerializer, 
    ProductSerializer,
    PaginationSerializer,
    ProductSerializerViewSet
)

class ColorViewSet(viewsets.ModelViewSet):

    serializer_class = ColorsSerializer
    queryset = Colors.objects.all()


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializerViewSet
    queryset = Product.objects.all()
    pagination_class = PaginationSerializer

    def perform_create(self, serializer):
        serializer.save(
            video="https://www.youtube.com/watch?v=C6wA3qOiLNg&list=RDC6wA3qOiLNg&start_radio=1"
        )

    
    def list(self, request, *args, **kwargs):
        usuario = self.request.user
        queryset = Product.objects.productos_por_user(usuario)

        # ******** esta parte las borramos *******
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

