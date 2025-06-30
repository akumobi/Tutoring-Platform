
# Create your views here.
import requests
import uuid
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payment
from tutor_sessions.models import Session
from .serializers import PaymentSerializer
from django.conf import settings

class CreatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        session_id = request.data.get('session_id')
        amount = request.data.get('amount')  # In Naira
        if not session_id or not amount:
            return Response({'detail': 'session_id and amount are required'}, status=400)

        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({'detail': 'Session not found'}, status=404)

        # Generate a unique transaction ID
        tx_ref = str(uuid.uuid4())

        # Paystack expects amount in Kobo
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": request.user.email,
            "amount": int(float(amount) * 100),  # Convert to Kobo
            "reference": tx_ref,
            "callback_url": "http://localhost:8000/payments/verify/",
        }

        response = requests.post("https://api.paystack.co/transaction/initialize", json=data, headers=headers)
        res_data = response.json()

        if response.status_code != 200:
            return Response(res_data, status=response.status_code)

        # Save payment in pending state
        Payment.objects.create(
            session=session,
            student=request.user,
            tutor=session.tutor,
            amount=amount,
            transaction_id=tx_ref,
            status='pending',
        )

        return Response({
            "authorization_url": res_data['data']['authorization_url'],
            "access_code": res_data['data']['access_code'],
            "reference": tx_ref
        }, status=status.HTTP_201_CREATED)
