from django.shortcuts import render
from rest_framework import generics
from .models import License, Client, LicenseType, EmailsLog
from .serializers import LisencesSerializer, ClientSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import enviar_licencias_a_clientes
from django.core.mail import EmailMessage, get_connection
from django.http import JsonResponse

class LicenseList(generics.ListCreateAPIView):
    queryset = License.objects.all()
    serializer_class = LisencesSerializer
    def post(self, request, *args, **kwargs):
        try:
             
            data = request.data
            print(data['client'])
            License.objects.create( 
                client_id=data['client'],
                package=data['package'],
                license_type= LicenseType.__getitem__(data['license_type']).value,
                license_status=data['license_status'],
                expiration_datetime=data['expiration_datetime']       
            )
            return Response({'mensaje': 'Acción realizada con éxito', 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'Parámetro faltante o inválido'}, status=status.HTTP_400_BAD_REQUEST)


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    

class LisenceTrigger(APIView):
    def post(self, request, *args, **kwargs):
            try:
                enviar_licencias_a_clientes()
                return Response({'mensaje': 'Acción realizada con éxito'}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'error': 'Ocurrio un error'}, status=status.HTTP_400_BAD_REQUEST)
      

class EmailsLogsList(generics.ListCreateAPIView):
    def get(self, request, num_emails):
        emails = EmailsLog.objects.all().order_by('-sent_datetime')[:num_emails]
        emails_list = []
        for email in emails:
            emails_list.append({
                'subject': email.subject,
                'sender': email.sender,
                'recipient': email.recipient,
                'message': email.body,
                'sent_datetime': email.sent_datetime
            })
        return JsonResponse(emails_list, safe=False)