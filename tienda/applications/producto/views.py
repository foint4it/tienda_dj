# apps de terceros
from rest_framework.generics import (
    ListAPIView,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
#
from django.shortcuts import render

# local serializers
from .serializers import ProductSerializer

# local models
from .models import Product

class ListProductUser(ListAPIView):
    """ vista para listar productos por usuario creador """
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,) # solo verifica q el token existe, pertenece a un user, pero no interfiere en las lineas de codigo siguientes a diferencia del permission_class
    permission_classes = [IsAuthenticated] # ReadOnly, IsAdminUser

    def get_queryset(self):
        usuario = self.request.user
        # recuperando usuario
        print("**********usuario por token***********")
        print(usuario)
        return Product.objects.productos_por_user(usuario)


class ListProductoStok(ListAPIView):
    """
        Vista para lista productos con stok mayor a cero
    """
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return Product.objects.productos_con_stok()


class ListProductoGenero(ListAPIView):
    """
        Vista para lista productos por genero
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        genero = self.kwargs['gender'] # parametro desde la url       
        return Product.objects.productos_por_genero(genero)


class FiltrarProductos(ListAPIView):
    """
        Vista que lista productos en base a varios filtros
    """
    serializer_class = ProductSerializer

    def get_queryset(self):    
        varon = self.request.query_params.get('man', None)
        mujer = self.request.query_params.get('woman', None)
        nombre = self.request.query_params.get('name', None)
        # print("**********")
        # print(varon)
        # print(mujer)
        # print(nombre)
        return Product.objects.filtrar_productos(
            man=varon, 
            woman=mujer, 
            name=nombre
        )
        

        