from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.pagination import PageNumberPagination
from .models import Item
from .serializers import ItemSerializer, UserSerializer, LoginSerializer, SignupSerializer
from datetime import timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ItemListApiView(APIView):
    permission_classes = [IsAuthenticated]

    # @method_decorator(cache_page(60 * 15))  # Cache results for 15 minutes
    query_params = {
        'SKU': 'SKU',
        'name': 'name__icontains',
        'tags': 'tags',
        'category': 'category',
        'start_date': 'created__gte',
        'end_date': 'created__lte',
        'min_cost': 'cost__gte',
        'max_cost': 'cost__lte',
        'is_assembly': 'is_assembly',
        'is_component': 'is_component',
        'is_purchaseable': 'is_purchaseable',
        'is_sellable': 'is_sellable',
        'is_bundle': 'is_bundle',
    }

    @swagger_auto_schema(
        operation_description="Get a list of items",
        manual_parameters=[
            openapi.Parameter('SKU', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
            openapi.Parameter('name', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
            openapi.Parameter('tags', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
            openapi.Parameter('category', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
            openapi.Parameter('start_date', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('end_date', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('min_cost', openapi.IN_QUERY,
                              type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_cost', openapi.IN_QUERY,
                              type=openapi.TYPE_NUMBER),
            openapi.Parameter('is_assembly', openapi.IN_QUERY,
                              type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('is_component', openapi.IN_QUERY,
                              type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('is_purchaseable',
                              openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('is_sellable', openapi.IN_QUERY,
                              type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('is_bundle', openapi.IN_QUERY,
                              type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: ItemSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):

        items = Item.objects.filter(
            user_id=request.user.id).order_by('created')

        for param, field in self.query_params.items():
            value = request.GET.get(param)
            if value is not None:
                if 'date' in param:
                    value = parse_date(value)
                elif 'cost' in param:
                    value = float(value)
                elif field in ['is_assembly', 'is_component', 'is_purchaseable', 'is_sellable', 'is_bundle']:
                    value = value.lower() == 'true'
                items = items.filter(**{field: value})

        paginator = CustomPagination()
        paginated_items = paginator.paginate_queryset(items, request)
        serializer = ItemSerializer(paginated_items, many=True)

        return paginator.get_paginated_response(serializer.data)

    # Create
    @swagger_auto_schema(
        operation_description="Create a new item",
        request_body=ItemSerializer,
        responses={201: ItemSerializer}
    )
    def post(self, request, *args, **kwargs):
        data = {
            'user_id': request.user.id,
            'SKU': request.data.get('SKU'),
            'name': request.data.get('name'),
            'category': request.data.get('category'),
            'tags': request.data.get('tags'),
            'cost': request.data.get('cost'),
            'in_stock': request.data.get('in_stock'),
            'available_stock': request.data.get('available_stock'),
            'minimum_stock': request.data.get('minimum_stock'),
            'desired_stock': request.data.get('desired_stock'),
            'is_assembly': request.data.get('is_assembly'),
            'is_component': request.data.get('is_component'),
            'is_purchaseable': request.data.get('is_purchaseable'),
            'is_sellable': request.data.get('is_sellable'),
            'is_bundle': request.data.get('is_bundle')
        }
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update
    @swagger_auto_schema(
        operation_description="Update an item",
        request_body=ItemSerializer(partial=True),
        responses={200: ItemSerializer}
    )
    def put(self, request, *args, **kwargs):
        item = Item.objects.get(id=request.data.get('id'))

        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete an item",
        request_body=ItemSerializer(partial=True),
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        item_id = Item.objects.get(id=request.data.get('id'))
        item_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginApiView(APIView):
    authentication_classes = []  # disable authentication
    permission_classes = []  # disable permission
    csrf_exempt = True  # disable CSRF

    @swagger_auto_schema(
        operation_description="Login to the app",
        request_body=LoginSerializer,
        responses={200: UserSerializer}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            login(request, user)

            request.session.set_expiry(timedelta(days=1))
            return Response({
                'user': UserSerializer(user).data,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request):
    #     return render(request, 'login.html')


class SignupApiView(APIView):
    authentication_classes = []  # disable authentication
    permission_classes = []  # disable permission
    csrf_exempt = True  # disable CSRF

    @swagger_auto_schema(
        operation_description="Signup to the app",
        request_body=SignupSerializer,
        responses={200: UserSerializer}
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        login(request, user)
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Signup successful'
        })


class LogoutApiView(APIView):
    authentication_classes = []  # disable authentication
    permission_classes = []  # disable permission
    csrf_exempt = True  # disable CSRF

    @swagger_auto_schema(
        operation_description="Logout from the app",
        responses={200: 'Logged out successfully'}
    )
    def post(self, request):
        logout(request)
        return Response({
            'message': 'Logged out successfully'
        })
