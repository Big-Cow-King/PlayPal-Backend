import json

import requests
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event
from payments.models import Payment
from payments.serializers import PaymentSerializer

PAYPAL_CLIENT_ID = 'ATAHRPKshzdr3W5stAzAKRXBGr8RCcyC5Hi8M3Dklap0VWUFQAQzBTd1oOs9ldwNsxXDJRIx0WoG_fzv'
ENCRYPT_S = 'LOsKj0ijuz0RQmFRrPx5zQrRBKx32JSC1IpyZ7zqk2-yKpA4Aa71SvktYuQ52sIyekZBvsx5EQnCIVLE'


def rotate_secret(secret):
    return secret[-1] + secret[:-1]


def get_access_token():
    url = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data,
                             auth=(PAYPAL_CLIENT_ID, rotate_secret(ENCRYPT_S)))
    return response.json().get('access_token')


# Create your views here.
class PaymentListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.all().filter(user=self.request.user).order_by(
            '-date')


class CreatePaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        if not data.get('amount'):
            return Response({'error': 'Amount is required'}, status=400)
        if not data.get('event_id'):
            return Response({'error': 'Event ID is required'}, status=400)
        if not int(data.get('amount')) > 0:
            return Response({'error': 'Amount must be greater than 0'},
                            status=400)
        if not data.get('return_url'):
            return Response({'error': 'return_url is required'}, status=400)
        if not data.get('cancel_url'):
            return Response({'error': 'cancel_url is required'}, status=400)
        amount = data.get('amount')
        event_id = data.get('event_id')
        return_url = data.get('return_url')
        cancel_url = data.get('cancel_url')

        get_object_or_404(Event, id=event_id)

        access_token = get_access_token()
        url = 'https://api-m.sandbox.paypal.com/v2/checkout/orders'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        data = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "CAD",
                        "value": amount
                    }
                }
            ],
            "application_context": {
                "cancel_url": cancel_url,
                "return_url": return_url,
            }
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        Payment.objects.create(
            user=request.user,
            amount=amount,
            event_id=event_id,
            transaction_id=response.json().get('id')
        )
        response_to_client = {
            'id': response.json().get('id'),
            'status': response.json().get('status'),
            'link': next((d for d in response.json().get('links') if
                          d.get("rel") == "approve"), None)["href"]
        }
        return Response(response_to_client)


class PaymentVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order_id = request.query_params.get('token')
        if not order_id:
            return Response({'error': 'token is required'}, status=400)

        access_token = get_access_token()
        url = f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        if response.json().get('status') == 'APPROVED':
            payment = get_object_or_404(Payment, transaction_id=order_id,
                                        user=request.user)
            payment.status = 'Approved'
            payment.save()

            event = payment.event
            event.promotion += payment.amount
            event.save()
        return Response(json.loads(response.text))


class PaymentCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order_id = request.query_params.get('token')
        if not order_id:
            return Response({'error': 'token is required'}, status=400)

        payment = get_object_or_404(Payment, transaction_id=order_id,
                                    user=request.user)
        payment.status = 'Cancelled'
        payment.save()
        return Response({'message': 'Payment cancelled successfully'})
