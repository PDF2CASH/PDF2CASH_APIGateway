from django.test import TestCase
from .models import Worker
import json

# Create your tests here.


class WorkerTest(TestCase):
    url = '/api/worker/worker/'

    def setUp(self):
        self.worker1 = Worker.objects.create(
            name='João Carlos de Almeida',
            cpf='03827819400',
            email='joaocarlos@email.com',
            password='1234560212'
        )

    def as_dict(self):
        return {
            'id': self.worker1.id,
            'name': self.worker1.name,
            'cpf': self.worker1.cpf,
            'email': self.worker1.email,
            'password': self.worker1.password
        }

    def test_worker_object_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_worker_object_post(self):
        data = {
            'name': 'Carlos Alberto Rocha',
            'cpf': '94837284799',
            'email': 'carlosalberto@email.com',
            'password': '23847302'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        data['id'] = json.loads(response.content)['id']
        self.assertEqual(json.loads(response.content), data)

    def test_worker_object_delete(self):
        self.url += f'{self.worker1.id}/'
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        response = self.client.get('/api/worker/worker/')
        self.assertEqual(len(json.loads(response.content)), 0)

    def test_worker_object_read(self):
        self.url += f'{self.worker1.id}/'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), self.as_dict())

    def test_worker_object_partial_update(self):
        self.url += f'{self.worker1.id}/'
        data = json.dumps({
            "id": self.worker1.id,
            "name": "Roberto Junior Aragão",
            "cpf": "27491047355",
            "email": "robertojunior@email.com",
            "password": "483058492"
        })
        response = self.client.patch(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        Worker.objects.all().delete()
