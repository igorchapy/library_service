from django_q2.tasks import async_task
from .notifications import send_telegram_message


def notify_borrowing_created(user_email, book_title):
    async_task(
        send_telegram_message,
        f"📚 <b>New Borrowing:</b>\nUser: {user_email}\nBook: {book_title}"
    )

def notify_borrowing_overdue(user_email, book_title, days_overdue):
    async_task(
        send_telegram_message,
        f"⏰ <b>Overdue Borrowing:</b>\nUser: {user_email}\nBook: {book_title}\nOverdue: {days_overdue} days"
    )

def notify_payment_success(user_email, amount):
    async_task(
        send_telegram_message,
        f"💰 <b>Payment Successful:</b>\nUser: {user_email}\nAmount: ${amount}"
    )
