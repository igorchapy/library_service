from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


# ---------------------------
# USER MODEL
# ---------------------------
class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='library_user_set',  # Зміни related_name, щоб не було конфлікту
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='library_user_permissions_set',  # Теж змінити
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

# ---------------------------
# BOOK MODEL
# ---------------------------
class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "HARD", "Hardcover"
        SOFT = "SOFT", "Softcover"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=10, choices=CoverType.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.title} by {self.author}"

3
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowings")

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user.email}"


# ---------------------------
# PAYMENT MODEL
# ---------------------------
class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    status = models.CharField(max_length=10, choices=Status.choices)
    type = models.CharField(max_length=10, choices=Type.choices)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE, related_name="payments")

    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.type} - {self.status} (${self.money_to_pay})"
