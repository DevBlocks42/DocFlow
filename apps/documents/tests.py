from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Document

User = get_user_model()


class DocumentListTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            email="testuser@docflow.com",
            password="password123",
            role="employe"
        )

        # création de 30 documents pour pagination
        for i in range(30):
            Document.objects.create(
                title=f"Document {i}",
                status="draft",
                created_by=cls.user
            )

    def setUp(self):
        self.client.login(username="testuser@docflow.com", password="password123")
        self.url = reverse("list-documents")

    # ----------------------
    # Pagination
    # ----------------------

    def test_default_pagination(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        page = response.context["page_obj"]
        self.assertEqual(page.number, 1)
        self.assertEqual(len(page.object_list), 10)
        self.assertTrue(page.has_next())

    def test_second_page(self):

        response = self.client.get(self.url, {
            "page": 2
        })

        page = response.context["page_obj"]

        self.assertEqual(page.number, 2)

    def test_invalid_page(self):

        response = self.client.get(self.url, {
            "page": 999
        })

        self.assertEqual(response.status_code, 200)

    # ----------------------
    # Sorting
    # ----------------------

    def test_sort_ascending(self):

        response = self.client.get(self.url, {
            "sort_field": "title",
            "sort_order": "asc"
        })

        docs = list(response.context["page_obj"])

        titles = [doc.title for doc in docs]

        self.assertEqual(titles, sorted(titles))

    def test_sort_descending(self):

        response = self.client.get(self.url, {
            "sort_field": "title",
            "sort_order": "desc"
        })

        docs = list(response.context["page_obj"])

        titles = [doc.title for doc in docs]

        self.assertEqual(titles, sorted(titles, reverse=True))

    def test_invalid_sort_field(self):

        response = self.client.get(self.url, {
            "sort_field": "invalid_field"
        })

        self.assertEqual(response.status_code, 302)

    # ----------------------
    # Filtering
    # ----------------------

    def test_filter_status(self):

        response = self.client.get(self.url, {
            "filter_field": "status",
            "filter": "draft"
        })

        docs = response.context["page_obj"]

        for doc in docs:
            self.assertEqual(doc.status, "draft")

    def test_filter_title(self):

        response = self.client.get(self.url, {
            "filter_field": "title",
            "filter": "Document 1"
        })

        docs = response.context["page_obj"]

        for doc in docs:
            self.assertIn("Document 1", doc.title)

    # ----------------------
    # Combined tests
    # ----------------------

    def test_filter_and_sort(self):

        response = self.client.get(self.url, {
            "filter_field": "status",
            "filter": "Brouillon",
            "sort_field": "title",
            "sort_order": "desc"
        })

        docs = list(response.context["page_obj"])

        titles = [doc.title for doc in docs]

        self.assertEqual(titles, sorted(titles, reverse=True))

    def test_filter_sort_and_pagination(self):

        response = self.client.get(self.url, {
            "filter_field": "status",
            "filter": "Brouillon",
            "sort_field": "title",
            "sort_order": "asc",
            "page": 2
        })

        page = response.context["page_obj"]

        self.assertEqual(page.number, 2)