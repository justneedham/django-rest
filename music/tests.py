from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Songs
from .serializers import SongsSerializer

# Create your tests here.


class BaseViewTest(APITestCase):

    client = APIClient()

    @staticmethod
    def create_song(title="", artist=""):
        if title != "" and artist != "":
            Songs.objects.create(title=title, artist=artist)

    def setUp(self):
        # add test data
        self.create_song('Monster', 'Starset')
        self.create_song('The Stage', 'Avenged Sevenfold')
        self.create_song('Dead Inside', 'Muse')
        self.create_song('Bloodline', 'Crown The Empire')
        self.create_song('More To Life', 'Lightscape')
        self.create_song('Prayer Of The Refugee', 'Rise Against')
        self.create_song('Bloodflood Pt II', 'Alt-J')

class GetAllSongsTest(BaseViewTest):

    def test_get_all_songs(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint

        """

        # Hit the API Endpoint
        response = self.client.get(
            reverse('songs-all', kwargs={'version': 'v1'})
        )

        # Fetch data from db
        expected = Songs.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
