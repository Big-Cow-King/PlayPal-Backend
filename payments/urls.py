from django.urls import path

from payments.views import CreatePaymentAPIView, PaymentCancelView, \
    PaymentListAPIView, \
    PaymentVerifyView

urlpatterns = [
    path('list/', PaymentListAPIView.as_view(), name='payment-list'),
    path('create/', CreatePaymentAPIView.as_view(), name='payment-create'),
    path('verify/', PaymentVerifyView.as_view(), name='payment-verify'),
    path('cancel/', PaymentCancelView.as_view(), name='payment-cancel'),
]
