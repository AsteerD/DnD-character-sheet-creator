from django.test import TestCase # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.urls import reverse # type: ignore
from .models import Character


class CharacterDeleteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='deluser', password='pass')
        self.character = Character.objects.create(
            user=self.user,
            character_name='ToDelete',
            character_class='Fighter',
            subclass='None',
            race='Human',
            level=1,
            background='Acolyte',
            alligment='TN',
            armor_class=10,
            initiative=0,
            speed=30,
            hit_points=1,
            temporary_hit_points=0,
            hit_dice=1,
        )

    def test_delete_get_shows_confirmation(self):
        url = reverse('character-delete', args=[self.character.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Are you sure')

    def test_delete_post_deletes(self):
        url = reverse('character-delete', args=[self.character.pk])
        resp = self.client.post(url, follow=True)
        self.assertRedirects(resp, reverse('characters'))
        self.assertFalse(Character.objects.filter(pk=self.character.pk).exists())

