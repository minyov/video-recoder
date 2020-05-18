from django.test import TestCase
from django.shortcuts import reverse


class TestMainView(TestCase):
    def test_view(self):
        res = self.client.get(reverse('main'))

        self.assertEquals(res.status_code, 200)
