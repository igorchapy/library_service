from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import RequestFactory


from app.admin import UserAdmin # adjust path if needed


class MockAdminSite(AdminSite):
    pass




class UserAdminTests(TestCase):
    def setUp(self):
    self.site = MockAdminSite()
    self.admin = UserAdmin(get_user_model(), self.site)
    self.factory = RequestFactory()
    self.user = get_user_model().objects.create_user(
    email="test@example.com",
    password="password123",
    first_name="Test",
    last_name="User",
    )


def test_list_display(self):
    self.assertEqual(
    self.admin.list_display,
    ("email", "first_name", "last_name", "is_staff")
    )


def test_search_fields(self):
    self.assertEqual(
    self.admin.search_fields,
    ("email", "first_name", "last_name")
    )


def test_ordering(self):
    self.assertEqual(self.admin.ordering, ("email",))


def test_fieldsets_structure(self):
    fieldset_names = [fs[0] for fs in self.admin.fieldsets]
    self.assertIn(None, fieldset_names)
    self.assertIn("Personal info", fieldset_names)
    self.assertIn("Permissions", fieldset_names)
    self.assertIn("Important dates", fieldset_names)


def test_add_fieldsets(self):
    add_fieldset = self.admin.add_fieldsets[0]
    self.assertIn("fields", add_fieldset[1])
    self.assertEqual(
    add_fieldset[1]["fields"], ("email", "password1", "password2")
    )


def test_admin_changelist_page_loads(self):
    request = self.factory.get(
    reverse("admin:app_user_changelist") # adjust `app_user` to match your app
    )
    request.user = self.user
    response = self.admin.changelist_view(request)
    self.assertEqual(response.status_code, 200)
