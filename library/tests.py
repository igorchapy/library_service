from django.urls import path
from .views import (
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView,
    BorrowingListCreateAPIView,
    BorrowingRetrieveUpdateDestroyAPIView,
    PaymentListCreateAPIView,
    PaymentRetrieveUpdateDestroyAPIView,
)


app_name = "library"

urlpatterns = [
    # ---------- BOOKS ----------
    path(
        "books/",
        BookListCreateAPIView.as_view(),
        name="book-list-create"
    ),
    path(
        "books/<int:pk>/",
        BookRetrieveUpdateDestroyAPIView.as_view(),
        name="book-detail"
    ),

    # ---------- BORROWINGS ----------
    path(
        "borrowings/",
        BorrowingListCreateAPIView.as_view(),
        name="borrowing-list-create"
    ),
    path(
        "borrowings/<int:pk>/",
        BorrowingRetrieveUpdateDestroyAPIView.as_view(),
        name="borrowing-detail"
    ),

    # ---------- PAYMENTS ----------
    path(
        "payments/",
        PaymentListCreateAPIView.as_view(),
        name="payment-list-create"
    ),
    path(
        "payments/<int:pk>/",
        PaymentRetrieveUpdateDestroyAPIView.as_view(),
        name="payment-detail"
    ),
]
