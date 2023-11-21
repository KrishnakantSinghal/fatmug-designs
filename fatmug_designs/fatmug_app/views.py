from rest_framework import generics
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from .models import *

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
            serializer_class = self.get_serializer_class()
            vendor_id = self.kwargs.get("vendor_id", None)
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
        
    
