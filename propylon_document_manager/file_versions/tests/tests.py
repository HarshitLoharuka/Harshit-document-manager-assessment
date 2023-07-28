import json
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from propylon_document_manager.file_versions.models import FileVersion
from propylon_document_manager.users.models import User


class FileVersionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='harshit@propylon.com',
            password='Password_random'
        )
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_upload_file_invalid_method(self):
        url = '/api/upload-file/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response_data = response.json()
        self.assertEqual(response_data, {'detail': 'Method "GET" not allowed.'})

    def test_upload_file_missing_data(self):
        url = '/api/upload-file/'
        data = {}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertEqual(response_data, {'error': 'File name and file URL are required.'})

    def test_upload_file_success(self):
        url = '/api/upload-file/'
        data = {
            'file_name': 'offerletter.txt',
            'file_url': 'http://propylon.com/offerletter.txt'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertEqual(response_data, {'message': 'File version created successfully!'})

    def test_get_file_version_latest(self):
        # Add a file to the database before testing
        url = '/api/upload-file/'
        data = {
            'file_name': 'offerletter.txt',
            'file_url': 'http://propylon.com/offerletter.txt'
        }
        self.client.post(url, data, format='json')

        url = '/api/get-file-version/?file_name=offerletter.txt'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['file_name'], 'offerletter.txt')
        self.assertEqual(response_data['version_number'], 0)
        self.assertEqual(response_data['file_url'], 'http://propylon.com/offerletter.txt')

    def test_get_file_version_specific(self):
        url = '/api/get-file-version/?file_name=payslip.txt&revision=1'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.json()
        self.assertEqual(response_data, {'error': 'File not found.'})

    def test_get_unique_files(self):
        url = '/api/upload-file/'
        data = {
            'file_name': 'increment.txt',
            'file_url': 'http://propylon.com/increment.txt'
        }
        self.client.post(url, data, format='json')

        url = '/api/get-unique-files/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data, {'unique_files': ['increment.txt']})

    def test_get_file_versions(self):
        url = '/api/upload-file/'
        data = {
            'file_name': 'increment.txt',
            'file_url': 'http://propylon.com/increment.txt'
        }
        self.client.post(url, data, format='json')

        url = '/api/get-file-versions/?file_name=increment.txt'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data, {'file_name': 'increment.txt', 'versions': [0]})
