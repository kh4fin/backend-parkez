from rest_framework.decorators import api_view, permission_classes
import base64
from io import BytesIO
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Paket, Parking, TransaksiPaket, CheckInParkir
from .serializers import PaketSerializer, ParkingSerializer, TransaksiPaketSerializer, CheckInParkirSerializer
from .permissions import IsOwner, IsPartnerOrOwner, IsUserOrAbove
from rest_framework.response import Response
from .midtrans import create_midtrans_transaction
import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.urls import reverse

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
@permission_classes([IsAuthenticated, IsUserOrAbove])
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

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def midtrans_notification(request, transaksi_id):
    data = request.data
    transaction_status = data.get('transaction_status')

    # Cari transaksi berdasarkan ID
    try:
        transaksi = TransaksiPaket.objects.get(id=transaksi_id)
    except TransaksiPaket.DoesNotExist:
        return Response({'message': 'Transaksi tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)

    # Update status transaksi
    if transaction_status == 'settlement':
        transaksi.status = 'paid'
    elif transaction_status == 'pending':
        transaksi.status = 'pending'
    elif transaction_status in ['cancel', 'expire']:
        transaksi.status = 'failed'
    else:
        return Response({'message': 'Status pembayaran tidak valid'}, status=status.HTTP_400_BAD_REQUEST)

    transaksi.save()
    return redirect(f"http://localhost:5173/home")
    # return Response({'message': 'Status transaksi berhasil diperbarui'}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated, IsPartnerOrOwner])
# def midtrans_notification(request):
#     data = request.data
#     order_id = data.get('order_id', '').split('-')[-1]  
#     transaksi = get_object_or_404(TransaksiPaket, id=order_id)

#     print(data)

#     if data['status'] == 'settlement':
#         transaksi.status = 'paid'
#     elif data['transaction_status'] == 'pending':
#         transaksi.status = 'pending'
#     elif data['transaction_status'] in ['cancel', 'expire']:
#         transaksi.status = 'failed'
#     else:
#         return Response({'message': 'Status pembayaran tidak valid'}, status=status.HTTP_400_BAD_REQUEST)
    
#     transaksi.save()
#     return Response({'message': 'Pembayaran berhasil diperbarui'}, status=status.HTTP_200_OK)

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
    transaksi = TransaksiPaket.objects.all()
    serializer = TransaksiPaketSerializer(transaksi, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_transaksi_paket_by_User(request):
    user = request.user
    transaksi = TransaksiPaket.objects.filter(user=user)
    serializer = TransaksiPaketSerializer(transaksi, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_paket_user(request):
    user = request.user
    print(user)
    transaksi = TransaksiPaket.objects.filter(user=user, status='paid')
    print(transaksi)
    
    if not transaksi.exists():
        return Response({'message': 'Belum ada paket yang dibeli'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TransaksiPaketSerializer(transaksi, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_checkin_parkir(request):
    user = request.user
    checkin_parkir = CheckInParkir.objects.filter(user=user)
    serializer = CheckInParkirSerializer(checkin_parkir, many=True)
    return Response(serializer.data)

@api_view(['POST'])  
@permission_classes([IsAuthenticated])
def checkin_parkir(request, transaksi_id):
    transaksi = get_object_or_404(TransaksiPaket, id=transaksi_id)

    if transaksi.status != 'paid':
        return Response(
            {'message': 'Paket belum dibayar atau tidak valid'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    current_time = timezone.now()
    if current_time > transaksi.durasi_aktif:
        return Response(
            {'message': 'Paket telah expired', 'status': 'expired'}, 
            status=status.HTTP_200_OK
        )

    user_di_scan = transaksi.user

    parking_spot = Parking.objects.first()  

    checkin_record = CheckInParkir.objects.create(
        user=user_di_scan,
        parking=parking_spot,
    )

    serializer = CheckInParkirSerializer(checkin_record)

    return Response(
        {
            'message': 'Check-in berhasil',
            'user': user_di_scan.email,
            'paket': transaksi.paket.nama_paket,
            'checkin': serializer.data,
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsUserOrAbove])
def history_list_create(request):
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



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def generate_qrcode(request, transaksi_id):
#     user = request.user
#     transaksi = get_object_or_404(TransaksiPaket, id=transaksi_id, user=user)

#     url = request.build_absolute_uri(reverse('verify_qrcode', kwargs={'transaksi_id': transaksi.id}))

#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(url)
#     qr.make(fit=True)

#     img = qr.make_image(fill='black', back_color='white')

#     buffer = BytesIO()
#     img.save(buffer, 'PNG')
#     buffer.seek(0)

#     return HttpResponse(buffer, content_type='image/png')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_qrcode(request, transaksi_id):
    user = request.user
    transaksi = get_object_or_404(TransaksiPaket, id=transaksi_id, user=user)

    url = request.build_absolute_uri(reverse('checkin-parkir', kwargs={'transaksi_id': transaksi.id}))

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return Response({'qr_code_base64': img_base64})


@api_view(['GET'])
def verify_qrcode(request, transaksi_id):
    transaksi = get_object_or_404(TransaksiPaket, id=transaksi_id)

    if transaksi.status != 'paid':
        return Response({'message': 'Paket belum dibayar atau tidak valid'}, status=status.HTTP_400_BAD_REQUEST)

    current_time = timezone.now()
    if current_time > transaksi.durasi_aktif:
        return Response({'message': 'Paket telah expired', 'status': 'expired'}, status=status.HTTP_200_OK)

    paket_info = {
        'paket': transaksi.paket.nama,
        'harga': transaksi.paket.harga,
        'diskon': transaksi.paket.diskon,
        'durasi_aktif': transaksi.durasi_aktif,
        'status': 'success',
    }
    
    return Response(paket_info, status=status.HTTP_200_OK)


