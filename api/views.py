from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from home.models import Documents
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import BizData
# from .serializers import BizDataSerializer
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
import pandas as pd

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

# Create your views here.
class RegAPIView(APIView):
	def post(self, r):
		data = r.data
		if 'username' in data and 'password' in data and 'email' in data:
			user = User(username=data['username'], password=data['password'], email=data['email'])
			user.save()
			return Response({"detail": "Registration Successful."}, status=status.HTTP_200_OK)
		return Response({"detail": "Fields Missing."}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, r):
        username = r.data['username']
        password = r.data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(r, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        
        else:
            raise exceptions.AuthenticationFailed('No such user')

   
class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, r):
        user = r.user
        if user.is_authenticated:
            token = Token.objects.get(user=user)
            token.delete()
            # r.user.auth_token.delete()
            logout(r)
        return Response({"detail": "Logout Successful."}, status=status.HTTP_200_OK)
    

class UploadAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, r):
        user = r.user
        description_entered = r.data.get("description", "")
        uploaded_file = r.FILES['file']
        if uploaded_file is None or not description_entered:
            return Response({"error": "No file or description was submitted."}, status=status.HTTP_400_BAD_REQUEST)
        file_doc = Documents(user= user, file= uploaded_file, description= description_entered)
        file_doc.save()
        return Response({"file": "File Upload Successful."}, status=status.HTTP_200_OK)

class UpdateFileAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, r, file_id):
        try:
            fileobj = Documents.objects.get(pk= file_id)
        except:
            return Response({'error': 'File Does Not Exists.'}, status= status.HTTP_404_NOT_FOUND)
        
        file_to_be_updated = r.FILES.get('file')
        description = r.data.get("description", "")

        fileobj.file = file_to_be_updated
        fileobj.description = description

        fileobj.save()
        
        return Response({"details": "File Updated Successfully."}, status=status.HTTP_200_OK)
        

class DownloadAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, r, file_id):
        uploaded_file = Documents.objects.get(pk=file_id)
        response = HttpResponse(uploaded_file.file, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
        return response


class DeleteFileAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, r, file_id):
        try:
            document = Documents.objects.get(pk=file_id)
        
            if document.user == r.user:
                document.delete_document()
                return Response({"message": "File deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
            
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        
        except:
            return Response({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)


# class CSVUploadAPIView(APIView):
#     authentication_classes = [CsrfExemptSessionAuthentication]
#     permission_classes = [AllowAny]
#     parser_classes = (FileUploadParser,)

#     def post(self, request):
#         csv_file = request.FILES.get('file')
        
#         df = pd.read_csv(csv_file, delimiter=',', on_bad_lines='skip', skiprows=1)
#         data_list = df.to_dict(orient='records')
       
#         serializer = BizDataSerializer(data=data_list, many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Data uploaded successfully."}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CSVUploadAPIView(APIView):
    # authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser,)

    def post(self, r):
        csv_file = r.FILES.get('file')
        # csv_file['Content-Disposition'] = f'filename="{csv_file.file.name}"'

        df = pd.read_csv(csv_file, on_bad_lines='skip')
        # df['data_value'].fillna(0.0).astype(int)
        # df['magnitude'].fillna(0.0).astype(int)
        df= df.set_index('period')
        
        data_list = df.to_dict(orient='records')
        # for i in data_list:
        #     BizData

        instances = [BizData(**data) for data in data_list]

        BizData.objects.bulk_create(instances)

        # print (r.data)
        # return Response({'received data': r.data})
        # return Response({'received data': r.data})

        return Response({"message": "Data uploaded successfully."}, status=status.HTTP_201_CREATED)
