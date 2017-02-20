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

    def test_user_can_edit_category(self):
        """
        This test creates a category.

        It then edits the category with new details and asserts that;
            1. A category was created with the original name 'Mathematics'.
            2. A category has been edited with a new name 'English'.
            3. The user gets a feedback message when a Category has been edited.
            4. A status code of 200 (OK) is returned.
            5. The template 'category-edit' is used.
            6. That the maths_obj and eng_obj objects have the same id.
        """
        create_url = reverse('category-create')

        maths = {
            'name': 'Mathematics'
        }
        self.client.post(create_url, maths)
        # assert that category has been created
        math_obj = models.Category.objects.filter(name=maths['name'])[0]
        self.assertTrue(math_obj)

        english = {
            'name': 'English'
        }
        kwargs = {
            'categ_id': math_obj.id
        }
        edit_url = reverse('category-edit', kwargs=kwargs)
        response = self.client.post(edit_url, english)

        self.assertContains(
            response,
            '<p>Category of id {0} has been edited successfully!</p>'.format(
                math_obj.id),
            count=1,
            status_code=200,
            html=True
        )

        self.assertTemplateUsed(response, 'category-edit.html')

        # assert that object with name 'Mathematics' no longer exists
        no_math_obj = models.Category.objects.filter(name=maths['name'])
        self.assertFalse(no_math_obj)

        # assert that object with name 'English' exists
        eng_obj = models.Category.objects.filter(name=english['name'])[0]
        self.assertTrue(eng_obj)

        # assert that math_obj and eng_obj have same ID
        self.assertEqual(eng_obj.id, math_obj.id)

    def test_user_can_delete_categories(self):
        """
        This test creates a category and persists it to the database.

        Then assertion are made to ensure;
            1. that the aforementioned category is listed in the
            'available categories' section.
            2. that the category is deleted.
            3. that the category no longer appears in the 'available categories'
            when it has been deleted.
            4. that the category is no longer in the database.
        """
        # check to ensure that the database has no category entries
        categories = models.Category.objects.all()
        self.assertFalse(categories)

        # the reverse method takes in the name of a url and constructs the url.
        create_url = reverse('category-create')
        # create a Category (to be deleted later)
        cs = {
          'name': 'Computer Science'
        }
        response = self.client.post(create_url, cs)
        # It doesn't hurt to assert that the category has been persisted to
        # the database
        cs_obj = models.Category.objects.filter(name=cs['name'])[0]
        self.assertTrue(cs_obj)
        # assert that the category is listed amongst available categories
        self.assertContains(
            response,
            '<li>{0}</li>'.format(cs['name']),
            count=1,
            status_code=201,
            html=True
        )

        kwargs = {
            'categ_id': cs_obj.id
        }
        delete_url = reverse('category-delete', kwargs=kwargs)

        response = self.client.post(delete_url)

        self.assertContains(
            response,
            '<p>Category of id {0} does not exist!</p>'.format(
                cs_obj.id),
            count=1,
            status_code=200,
            html=True
        )

        self.assertTemplateUsed(response, 'category-delete.html')

        response = self.client.get(create_url)
        self.assertNotContains(
            response,
            '<li>{0}</li>'.format(cs['name']),
            status_code=200,
            html=True
        )

        # assert that the category has been deleted from the database
        deleted_categ = models.Category.objects.filter(name=cs['name'])
        self.assertFalse(deleted_categ)