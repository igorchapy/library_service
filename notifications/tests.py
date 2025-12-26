from unittest.mock import patch
from your_app.services import notify_borrowing_created
from your_app.notifications import send_telegram_message


@patch("your_app.services.async_task")
def test_notify_borrowing_created(mock_async_task):
    notify_borrowing_created(
        user_email="user@test.com",
        book_title="Django for Pros"
    )

    mock_async_task.assert_called_once_with(
        send_telegram_message,
        "📚 <b>New Borrowing:</b>\nUser: user@test.com\nBook: Django for Pros"
    )
