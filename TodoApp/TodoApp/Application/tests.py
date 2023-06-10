from django.test import TestCase

from TodoApp.Application.models import Assignment
from django.urls import reverse


# Create your tests here.

class TestToDoApp(TestCase):

    def test_index_when_no_todos(self):
        response = self.client.get('/')
        assignments = Assignment.objects.all()
        self.assertEqual(0, len(assignments))
        self.assertEqual(200, response.status_code)

    def test_index_when_existing_todos_to_display_expect_all_todos(self):
        entered_data1 = {
            'name': 'newtaksk1',
            "description": "something to do"
        }
        self.client.post(reverse('create_todo'), data=entered_data1)

        entered_data2 = {
            'name': 'newtaksk2',
            "description": "something to do 2"
        }
        self.client.post(reverse('create_todo'), data=entered_data2)

        response = self.client.get('/')

        self.assertEqual(2, len(response.context.dicts[3].get('todos')))
        self.assertEqual(200, response.status_code)

    def test_create_todo_expect_valid_data(self):
        entered_data = {
            'name': 'newtaksk1',
            "description": "something to do"
        }
        response = self.client.post(reverse('create_todo'), data=entered_data)
        todo = Assignment.objects.get(**entered_data)
        self.assertIsNotNone(todo)
        self.assertEqual("newtaksk1", todo.name)
        self.assertEqual("something to do", todo.description)
        self.assertEqual('/', response.headers.get('Location'))

    def test_create_new_task_already_exists(self):
        entered_data = {
            'name': 'newtaksk1',
            "description": "something to do"
        }
        self.client.post(reverse('create_todo'), data=entered_data)
        new_data = {
            'name': 'newtaksk1',
            "description": "something to do new"
        }
        response = self.client.post(reverse('create_todo'), data=new_data)
        self.assertEqual('Assignment with this Name already exists.',
                         response.context[2].dicts[1].get('errors')[0])

    def test_edit_todo_url_expect_redirect(self):
        entered_data = {
            'name': 'newtaksk1',
            "description": "something to do"
        }
        self.client.post(reverse('create_todo'), data=entered_data)
        todo = Assignment.objects.get(**entered_data)

        response = self.client.get(f"/edit/{todo.pk}/")
        self.assertEqual(200, response.status_code)

    def test_edit_todo_expect_data_to_change(self):
        entered_data = {
            'name': 'newtaksk1',
            "description": "something to do"
        }
        self.client.post(reverse('create_todo'), data=entered_data)
        todo = Assignment.objects.get(**entered_data)

        new_data = {
            'name': 'changed task',
            "description": "something to do changed"
        }

        response = self.client.post(reverse('edit', kwargs={'pk': todo.pk}), data=new_data)

        new_todo = Assignment.objects.get(**new_data)
        self.assertEqual('changed task', new_todo.name)
        self.assertEqual("something to do changed", new_todo.description)
        self.assertEqual('/', response.headers.get('Location'))

    def test_delete_todo_expect_todo_gone_redirect_to_index(self):
        entered_data = {
            'name': 'newtaksk1',
            "description": "something to do"
        }
        self.client.post(reverse('create_todo'), data=entered_data)
        todo = Assignment.objects.get(**entered_data)

        response = self.client.get(f"/delete/{todo.pk}/")

        self.assertEqual(0, len(Assignment.objects.all()))
        self.assertEqual('/', response.headers.get('Location'))

    def test_file_download(self):
        entered_data = {
            'name': 'newtaksk1',
            "description": "something to do"
        }
        self.client.post(reverse('create_todo'), data=entered_data)
        response = self.client.get('/download/')
        self.assertEqual(200, response.status_code)
        self.assertEqual('attachment; filename=tasks.txt', response.headers.get('Content-Description'))
        self.assertEqual('text/plain', response.headers.get('Content-Type'))
