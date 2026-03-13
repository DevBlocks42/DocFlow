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
        response = self.client.get(self.url, {"sort_field": "title", "sort_order": "asc"}, follow=True)
        page = response.context["page_obj"]

        # récupérer tout le queryset trié
        qs_sorted = Document.objects.all().order_by("title")
        expected_titles = [doc.title for doc in qs_sorted][:len(page.object_list)]

        page_titles = [doc.title for doc in page.object_list]

        self.assertEqual(page_titles, expected_titles)

    def test_sort_descending(self):
        response = self.client.get(self.url, {"sort_field": "title", "sort_order": "desc"}, follow=True)
        page = response.context["page_obj"]

        qs_sorted = Document.objects.all().order_by("-title")
        expected_titles = [doc.title for doc in qs_sorted][:len(page.object_list)]
        page_titles = [doc.title for doc in page.object_list]

        self.assertEqual(page_titles, expected_titles)

    def test_invalid_sort_field(self):
        # comme ta view redirige sur invalid sort_field
        response = self.client.get(self.url, {"sort_field": "invalid_field"}, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("list-documents"), response.url)

    # ----------------------
    # Filtering
    # ----------------------

    def test_filter_status(self):
        response = self.client.get(self.url, {"filter_field": "status", "filter": "Brouillon"}, follow=True)
        page = response.context["page_obj"]

        for doc in page.object_list:
            self.assertEqual(doc.status, "draft")

    def test_filter_title(self):
        response = self.client.get(self.url, {"filter_field": "title", "filter": "Document 1"}, follow=True)
        page = response.context["page_obj"]

        for doc in page.object_list:
            self.assertIn("Document 1", doc.title)

    # ----------------------
    # Combined tests
    # ----------------------

    def test_filter_and_sort(self):
        response = self.client.get(
            self.url,
            {"filter_field": "status", "filter": "Brouillon", "sort_field": "title", "sort_order": "desc"},
            follow=True,
        )
        page = response.context["page_obj"]

        qs_sorted = Document.objects.filter(status="draft").order_by("-title")
        expected_titles = [doc.title for doc in qs_sorted][:len(page.object_list)]
        page_titles = [doc.title for doc in page.object_list]

        self.assertEqual(page_titles, expected_titles)

    def test_filter_sort_and_pagination(self):
        response = self.client.get(
            self.url,
            {
                "filter_field": "status",
                "filter": "Brouillon",
                "sort_field": "title",
                "sort_order": "asc",
                "page": 2,
            },
            follow=True,
        )
        page = response.context["page_obj"]

        qs_sorted = Document.objects.filter(status="draft").order_by("title")
        expected_titles = [doc.title for doc in qs_sorted][10:20]  # page 2
        page_titles = [doc.title for doc in page.object_list]

        self.assertEqual(page_titles, expected_titles)