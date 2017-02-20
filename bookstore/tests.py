from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from bookstore import models


class BookstoreTests(TestCase):
    """
    This class contains tests for the bookstore app.
    """

    def setUp(self):
        """
        This method runs before the execution of each test case.
        """
        self.client = Client()

    def test_user_can_create_categories(self):
        """
        This test first checks that no categories exist in the database.

        It then creates a 'Science Fiction' and 'Programming' category and
        asserts that;
            1. the response code for both cases is HTTP 201 (Created)
            2. that the user receives feedback from the page when the category
                is created
            3. that the category-create.html template has been used
            4. that the category entries have been created in the database
            5. that the created categories have been rendered on the
            category-create.html template
        """
        # check to ensure that the database has no category entries
        categories = models.Category.objects.all()
        self.assertFalse(categories)

        # the reverse method takes in the name of a url and constructs the url.
        create_url = reverse('category-create')

        # create a Science Fiction category
        scifi = {
          'name': 'Science Fiction'
        }
        response = self.client.post(create_url, scifi)

        # assert that a feedback message indicating category creation is
        # displayed once and that the status code is 201
        self.assertContains(
            response,
            '<p>Category: {0} created!</p>'.format(scifi['name']),
            count=1,
            status_code=201,
            html=True
        )

        self.assertTemplateUsed(response, 'category-create.html')

        # check to confirm that one category (Science Fiction) has been
        # created in the database
        categ = models.Category.objects.filter(name=scifi['name'])
        self.assertEqual(len(categ), 1)
        self.assertTrue(isinstance(categ[0], models.Category))

        # create a programming category
        programming = {
          'name': 'Programming'
        }
        response = self.client.post(create_url, programming)

        # assert that a feedback message indicating category creation is
        # displayed once and that the status code is 201
        self.assertContains(
            response,
            '<p>Category: {0} created!</p>'.format(programming['name']),
            count=1,
            status_code=201,
            html=True
        )

        self.assertTemplateUsed(response, 'category-create.html')

        # check to confirm that a second entry (Programming) has been
        # created in the database
        categ = models.Category.objects.filter(name=programming['name'])
        self.assertTrue(isinstance(categ[0], models.Category))

        # check to confirm that there exists 2 Categories in the database
        categories = models.Category.objects.all()
        self.assertEqual(len(categories), 2)

        # check that the created categories are listed on the
        # category-create.html template
        response = self.client.get(create_url)
        self.assertContains(
            response,
            '<li>{0}</li>'.format(scifi['name']),
            count=1,
            status_code=200,
            html=True
        )
        self.assertContains(
            response,
            '<li>{0}</li>'.format(programming['name']),
            count=1,
            status_code=200,
            html=True
        )
