from rest_framework import generics
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from .models import *
from django.contrib.auth import authenticate


class AdminTokensView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token = CustomTokenObtainPairSerializer.get_token(user)
            response_dict = {
                'token': token,
                'msg': 'Admin login Success'
            }
            return Response({"code": 200, "data":response_dict}, status=status.HTTP_200_OK)
        else:
            return Response({"code": 404, 'errors': 'Email or Password is not Valid'},
                        status=status.HTTP_404_NOT_FOUND)


    
# Create your views here.
class VenderAPIView(generics.GenericAPIView):
    serializer_class = VendorSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        class VendorRetrieveSerializer(self.serializer_class):
            class Meta:
                model = self.serializer_class.Meta.model
                fields = "__all__"
        return VendorRetrieveSerializer


    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception = True):
                serializer.save()
                return Response({"message": "Vender Created Successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get(self, request, vendor_id=None):
        try:
            if vendor_id:
                vendors = Vendor.objects.get(id=vendor_id)
                serializer_class = self.get_serializer_class()
                serializer = serializer_class(vendors)

            else:
                vendors = Vendor.objects.all()
                serializer = self.serializer_class(vendors, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, vendor_id=None):
        try:
            if vendor_id:
                vendor = Vendor.objects.get(id=vendor_id)
                serializer = self.serializer_class(data=request.data, instance=vendor, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({"message": "Your details are updated successfully"}, status=status.HTTP_200_OK)

            else:
                return Response({"error": "Enter a valid vendor_id"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, vendor_id=None):
        try:
            if vendor_id:
                vendor = Vendor.objects.get(id=vendor_id)
                vendor.delete()
                return Response({"message": "vendor deleted successfully"}, status=status.HTTP_200_OK)

            else:
                return Response({"error": "Enter a valid vendor ID"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class PurchaseOrderView(generics.ListAPIView):
    serializer_class = PurchaseOrderSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "Purchase Order Created Successfully"})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_queryset(self):
        vendor_id = self.request.GET.get("vendor_id", None)
        purchase_order_id = self.kwargs.get("po_id", None)
        if vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
            return purchase_orders
        
        if purchase_order_id:
            purchase_orders = PurchaseOrder.objects.filter(id=purchase_order_id)
            return purchase_orders
        
        purchase_orders = PurchaseOrder.objects.all()
        return purchase_orders
        
    def put(self, request, *args, **kwargs):
        try:
            data = request.data
            po_id = kwargs.get("po_id")
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            serializer = self.serializer_class(data=request.data, instance = purchase_order, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"message": "Purchase Order Updated Successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def delete(self, request, po_id = None):
        try:
            purchase_order = PurchaseOrder.objects.get(id = po_id)
            purchase_order.delete()
            return Response({"message": "Purchase Order Successfully Deleted"}, status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        

class PerformanceMetricsView(generics.GenericAPIView):
    serializer_class = VendorSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        class PurchaseMetricsSerializer(self.serializer_class):
            class Meta:
                model = self.serializer_class.Meta.model
                fields = ["on_time_delivery_rate", "quality_rating_avg", "average_response_time", "fulfillment_rate"]
        return PurchaseMetricsSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            vendor_id = kwargs.get("vendor_id")
            vendor = Vendor.objects.get(id=vendor_id)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    


class AcknowledgePOView(generics.GenericAPIView):
    serializer_class = PurchaseOrderSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        try:
            po_id = kwargs.get("po_id")
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            purchase_order.acknowledgment_date = timezone.now()
            if not purchase_order.status == "complete":
                purchase_order.status == "complete"
                purchase_order.save()
                create_performance_matrics(purchase_order.vendor)
                return Response({"message": "Acknowledgement updated successfully"}, status=status.HTTP_200_OK)

            return Response({"error": "This Purchase Order is already acknowledged"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    