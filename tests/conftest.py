import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from unittest.mock import patch

from app.admin import UserAdmin
from your_app.notifications import send_telegram_message


class MockAdminSite(AdminSite):
    pass


@pytest.fixture
def admin_user(db):
    return get_user_model().objects.create_superuser(
        email="admin@test.com",
        password="password123",
    )


@pytest.fixture
def user_admin():
    site = MockAdminSite()
    return UserAdmin(get_user_model(), site)


@pytest.fixture
def rf():
    return RequestFactory()


@pytest.fixture
def mock_async_task():
    with patch("your_app.services.async_task") as mock:
        yield mock


@pytest.fixture
def telegram_sender():
    return send_telegram_message
