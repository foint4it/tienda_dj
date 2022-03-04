#
from rest_framework import serializers
#
from .models import Sale, SaleDetail


class VentaReporteSerializers(serializers.ModelSerializer):
    """ serializador para ver las ventas en detalle """

    productos = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = (
            'id',
            'date_sale',
            'amount',
            'count',
            'type_invoce',
            'cancelado',
            'type_payment',
            'state',
            'adreese_send',
            'user',
            'productos',
        )
    
    def get_productos(self, obj):
        queryset = SaleDetail.objects.productos_por_venta(obj.id)
        return DetalleVentaProductoSerializer(queryset, many=True).data

    # def get_type_invoce(self, obj):
    #     return obj.get_type_invoce_display()

class DetalleVentaProductoSerializer(serializers.ModelSerializer):
    """ serializdor para ver las ventas en detalle """

    product = serializers.CharField(source='product.name')
    class Meta:
        model = SaleDetail
        fields = (
            'id',
            'sale',
            'product',
            'count',
            'price_purchase',
            'price_sale',
        )


class ProductDetailSerializers(serializers.Serializer):
    """  formato para una lista de tipo serializador """
    
    pk = serializers.IntegerField()
    count = serializers.IntegerField()


class ProcesoVentaSerializer(serializers.Serializer):
    """ Serialziador para recibir una venta"""

    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    productos = ProductDetailSerializers(many=True)


class ArrayIntegerListSerializer(serializers.ListField):
    """  formato para una lista de tipo serializador array """
    
    child = serializers.IntegerField()


class ProcesoVentaSerializer2(serializers.Serializer):
    """ Serialziador para recibir una venta"""

    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    productos = ArrayIntegerListSerializer()
    cantidades = ArrayIntegerListSerializer()

    # 2 ejemplos de validar (poner los Or pythonicos correspondientes )
    def validate(self, data):
        if data['type_payment'] != '0':
            raise serializers.ValidationError('Ingrese un Tipo Pago correcto')
        return data

    def validate_type_invoce(self, value):
        if value != '0':
            raise serializers.ValidationError('Ingrese un Tipo Comprobante correcto')
        return value
