from django.test import TestCase
from django.shortcuts import reverse


class TestHealthCheck(TestCase):
    def test_view(self):
        res = self.client.get(reverse('health-check'))

        self.assertEquals(res.status_code, 200)
