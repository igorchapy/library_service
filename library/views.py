from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Book, Borrowing, Payment
from .serializers import BookSerializer, BorrowingSerializer, PaymentSerializer


# ---------------------------
# Custom Permission
# ---------------------------
class IsAdminOrIfAuthenticatedReadOnly(IsAuthenticated):
    """Дозволяє GET для всіх автентифікованих користувачів,
    а зміни — лише для staff."""
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff


# ---------------------------
# BOOK VIEWSET
# ---------------------------
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @extend_schema(
        parameters=[
            OpenApiParameter("author", OpenApiTypes.STR, description="Filter by author name"),
            OpenApiParameter("title", OpenApiTypes.STR, description="Filter by title"),
            OpenApiParameter("cover", OpenApiTypes.STR, description="Filter by cover type (HARD / SOFT)"),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        author = request.query_params.get("author")
        title = request.query_params.get("title")
        cover = request.query_params.get("cover")

        if author:
            queryset = queryset.filter(author__icontains=author)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if cover:
            queryset = queryset.filter(cover=cover.upper())

        self.queryset = queryset
        return super().list(request, *args, **kwargs)


# ---------------------------
# BORROWING VIEWSET
# ---------------------------
class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Staff бачить усі позики, звичайні користувачі — тільки свої."""
        user = self.request.user
        queryset = Borrowing.objects.select_related("book", "user")

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        # query params: active=true, user_id=, book_id=
        active = self.request.query_params.get("active")
        book_id = self.request.query_params.get("book_id")
        user_id = self.request.query_params.get("user_id")

        if active == "true":
            queryset = queryset.filter(actual_return_date__isnull=True)
        if book_id:
            queryset = queryset.filter(book_id=book_id)
        if user.is_staff and user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter("active", OpenApiTypes.BOOL, description="Show only active borrowings"),
            OpenApiParameter("book_id", OpenApiTypes.INT, description="Filter by book id"),
            OpenApiParameter("user_id", OpenApiTypes.INT, description="Filter by user id (staff only)"),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# ---------------------------
# PAYMENT VIEWSET
# ---------------------------
class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Staff бачить усі платежі, користувач — тільки свої."""
        user = self.request.user
        queryset = Payment.objects.select_related("borrowing", "borrowing__user")

        if not user.is_staff:
            queryset = queryset.filter(borrowing__user=user)

        # query params: status=PAID/PENDING, type=PAYMENT/FINE
        status_param = self.request.query_params.get("status")
        type_param = self.request.query_params.get("type")

        if status_param:
            queryset = queryset.filter(status=status_param.upper())
        if type_param:
            queryset = queryset.filter(type=type_param.upper())

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter("status", OpenApiTypes.STR, description="Filter by payment status (PENDING/PAID)"),
            OpenApiParameter("type", OpenApiTypes.STR, description="Filter by payment type (PAYMENT/FINE)"),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
