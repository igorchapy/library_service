from rest_framework import serializers
from .models import User, Book, Borrowing, Payment
from notifications.tasks import notify_borrowing_created


# ---------------------------
# USER SERIALIZER
# ---------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "is_staff"]


# ---------------------------
# BOOK SERIALIZER
# ---------------------------
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "cover", "inventory", "daily_fee"]


# ---------------------------
# BORROWING SERIALIZER
# ---------------------------
class BorrowingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # показує info про користувача
    book = BookSerializer(read_only=True)  # показує info про книгу
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source="book", write_only=True
    )

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "book_id",
            "user",
        ]

    def create(self, validated_data):
        # автоматично присвоюємо користувача з request
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user
        notify_borrowing_created(request.user.email, book_title=validated_data["book_title"])
        return super().create(validated_data)


# ---------------------------
# PAYMENT SERIALIZER
# ---------------------------
class PaymentSerializer(serializers.ModelSerializer):
    borrowing = BorrowingSerializer(read_only=True)
    borrowing_id = serializers.PrimaryKeyRelatedField(
        queryset=Borrowing.objects.all(), source="borrowing", write_only=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "type",
            "borrowing",
            "borrowing_id",
            "session_url",
            "session_id",
            "money_to_pay",
        ]
