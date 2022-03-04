from datetime import datetime
#
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
#
from django.utils import timezone
from django.shortcuts import get_object_or_404
#
from applications.producto.models import Product
#
from .models import Sale, SaleDetail
#
from .serializers import (
    VentaReporteSerializers,
    ProcesoVentaSerializer2
)


class VentasViewSet(viewsets.ViewSet):
    """
        Vista para registrar ViewSet
    """
    authentication_classes = (TokenAuthentication,)
    #permission_classes = [IsAuthenticated]
    #serializer_class = VentaReporteSerializers
    queryset = Sale.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if (self.action == 'list') or (self.action == 'retrieve'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    
    def list(self, request, *args,**kwargs):
        queryset = Sale.objects.all()
        serializer = VentaReporteSerializers(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        venta = get_object_or_404(Sale.objects.all(), pk=pk)
        serializer = VentaReporteSerializers(venta)
        return Response(serializer.data)


    def create(self, request):
        serializer = ProcesoVentaSerializer2(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        amount = 0 # monto total de venta
        count = 0
        venta = Sale.objects.create(
            date_sale=timezone.now(),
            amount=amount,
            count=count,
            type_invoce=serializer.validated_data['type_invoce'],
            type_payment=serializer.validated_data['type_payment'],
            adreese_send=serializer.validated_data['adreese_send'],
            state='3',
            user=self.request.user,
        )
        # recuperamos los productos de la venta
        productos = Product.objects.filter(
            id__in=serializer.validated_data['productos']
        )
        #
        cantidades = serializer.validated_data['cantidades']
        ventas_detalle = []
        for producto, cantidad in zip(productos, cantidades):
            # recue
            venta_detalle = SaleDetail(
                sale=venta,
                product=producto,
                count=cantidad,
                price_purchase=producto.price_purchase,
                price_sale=producto.price_sale,
            )
            #
            ventas_detalle.append(venta_detalle)
            #
            amount = amount + producto.price_sale
            count = count + cantidad
        #
        venta.amount = amount
        venta.count = count
        venta.save()
        #
        SaleDetail.objects.bulk_create(ventas_detalle)
        return Response({'msj': 'venta ok'})
