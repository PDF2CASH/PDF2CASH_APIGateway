from django.test import TestCase
from .models import Worker
import json

# Create your tests here.


class WorkerTest(TestCase):
    url = '/api/worker/worker/'

    def setUp(self):
        self.worker1 = Worker.objects.create_user(
            username='aloaloalo',
            cpf='94837284799',
            email='carlosalberto@email.com',
            password='12345678',
            permission='1'
        )

        response = self.client.post(
            '/api/authenticate/',
            json.dumps({
                'username': 'aloaloalo',
                'password': '12345678'
            }),
            content_type='application/json'
        )
        self.token = json.loads(response.content)['token']

    def as_dict(self):
        return {
            'id': self.worker1.id,
            'username': self.worker1.username,
            'cpf': self.worker1.cpf,
            'email': self.worker1.email,
            'password': self.worker1.password,
            'permission': self.worker1.permission
        }

    def test_worker_object_get(self):
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION='JWT {}'.format(self.token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_worker_object_post(self):
        data = {
            'username': 'aloaloaloalo',
            'cpf': '94831284799',
            'email': 'danielmarques786@gmail.com',
            'password': '123456789',
            'permission': '1'
        }

        response = self.client.post(
            self.url,
            json.dumps(data),
            HTTP_AUTHORIZATION='JWT {}'.format(self.token),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        data['id'] = json.loads(response.content)['id']

    def test_admin_object_post(self):
        data = {
            'username': 'victormota',
            'cpf': '94837284119',
            'email': 'victormota@email.com',
            'password': '12345678',
            'permission': '2'
        }

        response = self.client.post(
            self.url,
            json.dumps(data),
            HTTP_AUTHORIZATION='JWT {}'.format(self.token),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)

        data2 = {
            'username': 'joaopedro',
            'cpf': '94837544119',
            'email': 'joaopedro@email.com',
            'password': '12345678',
            'permission': '2'
        }

        response = self.client.post(
            self.url,
            json.dumps(data2),
            HTTP_AUTHORIZATION='JWT {}'.format(self.token),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)

    def test_worker_object_delete(self):
        self.url += f'{self.worker1.id}/'
        response = self.client.delete(
            self.url,
            HTTP_AUTHORIZATION='JWT {}'.format(self.token)
        )
        self.assertEqual(response.status_code, 204)

    def test_worker_object_read(self):
        self.url += f'{self.worker1.id}/'
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION='JWT {}'.format(self.token)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), self.as_dict())

    def test_worker_object_partial_update(self):
        self.url += f'{self.worker1.id}/'
        data = {
            'id': self.worker1.id,
            'username': 'aloaloaaaaaa',
            'cpf': '27491047355',
            'email': 'robertojunior@email.com',
            'password': '483058492',
            'permission': '1'
        }
        response = self.client.post(
            self.url,
            json.dumps(data),
            HTTP_AUTHORIZATION='JWT {}'.format(self.token),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

    def test_refresh_jwt_token(self):
        response = self.client.post(
            '/api/refresh/',
            json.dumps({
                'token': self.token,
            }), content_type='application/json'
        )

        self.assertIsInstance(json.loads(response.content), dict)

    def test_verify_jwt_token(self):
        response = self.client.post(
            '/api/api-token-verify/',
            json.dumps({
                'token': self.token,
            }), content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        Worker.objects.all().delete()
