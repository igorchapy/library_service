from django.urls import path, include
from rest_framework.routers import DefaultRouter
from library.views import BookViewSet, BorrowingViewSet, PaymentViewSet


app_name = "library"

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'borrowings', BorrowingViewSet, basename='borrowing')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
