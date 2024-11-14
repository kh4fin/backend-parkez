from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Paket, Parking, TransaksiPaket, CheckInParkir
from .serializers import PaketSerializer, ParkingSerializer, TransaksiPaketSerializer, CheckInParkirSerializer
from .permissions import IsOwner, IsPartnerOrOwner, IsUserOrAbove
from rest_framework.response import Response
from .midtrans import create_midtrans_transaction

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsUserOrAbove])
def parking_list_create(request):
    if request.method == 'GET':
        parking = Parking.objects.all()
        serializer = ParkingSerializer(parking, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.role == 'owner':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ParkingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsOwner])
def parking_detail(request, pk):
    parking = get_object_or_404(Parking, pk=pk)

    if request.method == 'GET':
        serializer = ParkingSerializer(parking)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ParkingSerializer(parking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        parking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsUserOrAbove])
def paket_list_create(request):
    if request.method == 'GET':
        paket = Paket.objects.all()
        serializer = PaketSerializer(paket, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.role == 'owner':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PaketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsOwner])
def paket_detail(request, pk):
    paket = get_object_or_404(Paket, pk=pk)

    if request.method == 'GET':
        serializer = PaketSerializer(paket)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = PaketSerializer(paket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        paket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsUserOrAbove])
def beli_paket(request):
    user = request.user
    paket_id = request.data.get('paketId')
    paket = get_object_or_404(Paket, id=paket_id)

    durasi_aktif = timezone.now() + timedelta(days=paket.durasi_hari)

    transaksi = TransaksiPaket.objects.create(user=user, paket=paket, durasi_aktif=durasi_aktif)

    order_id = f"order-{transaksi.id}"
    gross_amount = float(paket.harga - (paket.harga * paket.diskon / 100))

    midtrans_url, snap_token = create_midtrans_transaction(order_id, gross_amount, user)

    return Response({
        'message': 'Transaksi berhasil dibuat, lanjutkan pembayaran',
        'midtrans_url': midtrans_url,
        'snapToken': snap_token,
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsPartnerOrOwner])
def midtrans_notification(request):
    data = request.data
    if data['transaction_status'] == 'settlement':
        transaksi = get_object_or_404(TransaksiPaket, id=data['order_id'].split('-')[-1])
        transaksi.status = 'paid'
        transaksi.save()
        return Response({'message': 'Pembayaran diterima'}, status=status.HTTP_200_OK)
    return Response({'message': 'Pembayaran gagal'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsUserOrAbove])
def checkin_parkir(request):
    user = request.user
    parking_id = request.data.get('parking_id')
    parking = get_object_or_404(Parking, id=parking_id)

    CheckInParkir.objects.create(user=user, parking=parking)

    return Response({'message': 'Check-in berhasil'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_transaksi_paket(request):
    user = request.user
    transaksi = TransaksiPaket.objects.filter(user=user)
    serializer = TransaksiPaketSerializer(transaksi, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_checkin_parkir(request):
    user = request.user
    checkin_parkir = CheckInParkir.objects.filter(user=user)
    serializer = CheckInParkirSerializer(checkin_parkir, many=True)
    return Response(serializer.data)