from email import header
import email
from tkinter.tix import Tree
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from urllib import response
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
import requests
# Create your tests here.
from rest_framework_simplejwt.tokens import RefreshToken


class MovieTestCase(APITestCase):

    @property
    def bearer_token(self):
        # assuming there is a user in User model
        user = User.objects.create_superuser(
            username="saugat", email="saugat@gmail.com", password="helloworld", )
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}

    def test_add_movie(self):
        response = self.client.post(
            '/list/movies/', data={"title": "test", "description": "hello world"}, **self.bearer_token)
        self.assertEqual(response.status_code, 200)

    def test_movie_list(self):
        response = self.client.get(
            '/list/movies/', **self.bearer_token)
        self.assertEqual(response.status_code, 200)

    def test_delete_movie(self):
        response = self.client.delete(
            '/list/movies/', data={"movieid": 1}, ** self.bearer_token)
        self.assertEqual(response.status_code, 200)

    def test_update_delete_movie(self):
        response = self.client.delete(
            '/list/movies/', data={"movieid": 1, "title": "superman", "description": "awesome"}, ** self.bearer_token)
        self.assertEqual(response.status_code, 200)


class RentTestCase(APITestCase):

    @property
    def bearer_token(self):
        # assuming there is a user in User model
        user = User.objects.create(
            username="saugat", email="saugat@gmail.com", password="helloworld")
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}

    def test_create_rent(self):
        response = self.client.post(
            '/rent/movie/', data={"movieid": 1}, ** self.bearer_token)
        self.assertEqual(response.status_code, 200)

    def test_delete_rent(self):
        response = self.client.delete(
            '/delete/movie/', data={"rentid": 1}, ** self.bearer_token)
        self.assertEqual(response.status_code, 200)

    def test_delete_rent(self):
        response = self.client.delete(
            '/delete/movie/', data={"rentid": 1}, ** self.bearer_token)
        self.assertEqual(response.status_code, 200)

    def test_get_rents(self):
        response = self.client.get('/rent/movie/', ** self.bearer_token)
        self.assertEqual(response.status_code, 200)
