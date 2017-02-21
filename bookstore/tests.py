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

    def test_user_can_create_book_under_category(self):
        """
        This tests checks that a user can create a book within an existing
        category.

        First, a Category, 'Programming', is created.
        Then a book, 'Java How To Program, , 4th Edition' is created within
        the Category aforementioned.
        Assertions are then made against;
            1. the feedback message displayed when a book is created.
            2. the presence of the book in the database.
            3. that the book retrieved from the database is an instance of
            models.Book.
            4. that the book is displayed amongst available books
        """
        create_category_url = reverse('category-create')
        programming = {
            'name': 'Programming'
        }
        response = self.client.post(create_category_url, programming)

        # It doesn't hurt to assert that the category has been persisted to
        # the database
        prog_obj = models.Category.objects.filter(name=programming['name'])
        self.assertTrue(prog_obj)

        create_book_url = reverse('book-create')

        jhtp4 = {
            'category': prog_obj[0].id,
            'title': 'Java, How To Program, 4th Edition'
        }
        response = self.client.post(create_book_url, jhtp4)

        self.assertContains(
            response,
            '<p>{0} added to {1} category!</p>'.format(
                jhtp4['title'], programming['name']),
            count=1,
            status_code=201,
            html=True
        )

        self.assertTemplateUsed(response, 'book-create.html')

        # fetch the book from the database and assert its truthy value
        created_book = models.Book.objects.filter(title=jhtp4['title'])[0]
        self.assertTrue(created_book)
        # also assert that the model object retrieved is an instance of Book
        # model
        self.assertTrue(isinstance(created_book, models.Book))
        # assert that the book is listed in the create-book page
        response = self.client.get(create_book_url)

        self.assertContains(
            response,
            '<li>{0} ({1})</li>'.format(
                created_book.title, created_book.category.name),
            count=1,
            status_code=200,
            html=True
        )

    def test_user_can_edit_book_title(self):
        """
        This test creates two categories i.e. 'English' and 'Mathematics' and
        then creates a book within the 'Mathematics' category.

        The book's category and title are then edited and then assertions are
        made against;
            1. the truthy value of the book's instance when it's fetched from
            the database
            2. the truthy value of the book with the edited title and category
             when it is fetched from the database.
            3. The presence of a feedback message when the book is edited.
            4. The template that is used for editing book details.
        """
        create_category_url = reverse('category-create')
        english = {
            'name': 'English'
        }
        self.client.post(create_category_url, english)
        # check that English category has been created in the database
        english_obj = models.Category.objects.filter(name=english['name'])[0]
        self.assertTrue(english_obj)

        maths = {
            'name': 'Mathematics'
        }
        self.client.post(create_category_url, maths)
        # check that Mathematics category has been created in the database
        maths_obj = models.Category.objects.filter(name=maths['name'])[0]
        self.assertTrue(maths_obj)

        create_book_url = reverse('book-create')
        # deliberately misspell book title and erroneously classify under Maths
        misspelt = {
            'category': maths_obj.id,
            'title': 'Enlgsih Adi'
        }
        self.client.post(create_book_url, misspelt)
        # check book has been created in db
        misspelt_obj = models.Book.objects.filter(
            title=misspelt['title'], category=maths_obj)
        self.assertTrue(misspelt_obj)
        # check that the book doesn't exist under English category
        misspelt_404 = models.Book.objects.filter(
            title=misspelt['title'], category=english_obj)
        self.assertFalse(misspelt_404)

        # edit the book
        kwargs = {
            'book_id': misspelt_obj[0].id
        }
        edit_book_url = reverse('book-edit', kwargs=kwargs)
        # correct spelling and correct category
        correct_spell = {
            'category': english_obj.id,
            'title': 'English Aid'
        }
        response = self.client.post(edit_book_url, correct_spell)

        self.assertContains(
            response,
            '<p>Edit successful!</p>',
            count=1,
            status_code=200,
            html=True
        )

        self.assertTemplateUsed(response, 'book-edit.html')

        # the misspelt version no longer exists
        misspelt_obj = models.Book.objects.filter(
            title=misspelt['title'], category=maths_obj)
        self.assertFalse(misspelt_obj)
        # the edited version exists instead
        correct_obj = models.Book.objects.filter(
            title=correct_spell['title'], category=english_obj)
        self.assertTrue(correct_obj)

    def test_user_can_delete_a_book(self):
        """
        This test creates a category within which a book is added.

        The book is then deleted and the following assertions are made;
            1. that the book has been removed from the database.
            2. that the page displays feedback to the user once the book is
            deleted.
            3. that the book no longer appears in the available books section.
            4. that the correct template was used when deleting the book.
        """
        create_category_url = reverse('category-create')
        programming = {
            'name': 'Programming'
        }
        response = self.client.post(create_category_url, programming)
        # It doesn't hurt to assert that the category has been persisted to
        # the database
        prog_obj = models.Category.objects.filter(name=programming['name'])[0]
        self.assertTrue(prog_obj)

        create_book_url = reverse('book-create')

        jhtp4 = {
            'category': prog_obj.id,
            'title': 'Java, How To Program, 4th Edition'
        }
        response = self.client.post(create_book_url, jhtp4)

        # now to delete the book
        jhtp4_obj = models.Book.objects.filter(title=jhtp4['title'])[0]
        kwargs = {
            'book_id': jhtp4_obj.id
        }
        delete_book_url = reverse('book-delete', kwargs=kwargs)

        response = self.client.post(delete_book_url)

        self.assertContains(
            response,
            '<p>Book: {0} deleted!</p>'.format(jhtp4_obj.title),
            count=1,
            status_code=200,
            html=True
        )
        self.assertTemplateUsed(response, 'book-delete.html')

        # assert the book does not exist
        deleted_book = models.Book.objects.filter(title=jhtp4['title'])
        self.assertFalse(deleted_book)

        # assert there is no book at all in the database
        all_books = models.Book.objects.all()
        self.assertFalse(all_books)

        # assert page handles request for non existent book
        # database has no books, so id of 1 obviously doesn't exist
        kwargs = {
            'book_id': 1
        }
        delete_book_url = reverse('book-delete', kwargs=kwargs)
        response = self.client.post(delete_book_url)

        self.assertContains(
            response,
            '<p>Book of id {0} does not exist!</p>'.format(kwargs['book_id']),
            count=1,
            status_code=200,
            html=True
        )
        self.assertTemplateUsed(response, 'book-delete.html')
        # assert that the book isn't listed amongst available books
        response = self.client.get(create_book_url)
        self.assertNotContains(
            response,
            '<li>{0} ({1})</li>'.format(jhtp4['title'], programming['name']),
            status_code=200,
            html=True
        )