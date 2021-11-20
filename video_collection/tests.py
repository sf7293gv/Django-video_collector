from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from .models import Video

class TestHomePage(TestCase):

    def test_app_title_message_shown_on_home(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'MMA Videos Collector')
    

class TestAddVideos(TestCase):
    
    def test_add_vid(self):
        valid_video = {
            'name': 'discord',
            'url': 'https://www.youtube.com/watch?v=j9NZf9Wcodk',
            'notes': 'disc'
        }
        url = reverse('add_video')
        response = self.client.post(url, data=valid_video, follow=True)

        self.assertTemplateUsed('video_collection/video_list.html')

        self.assertContains(response, 'discord')
        self.assertContains(response, 'disc')
        self.assertContains(response, 'https://www.youtube.com/watch?v=j9NZf9Wcodk')

        video_count = Video.objects.count()
        self.assertEqual(1, video_count)

        video = Video.objects.first()

        self.assertEqual('discord', video.name)
        self.assertEqual('disc', video.notes)
        self.assertEqual('https://www.youtube.com/watch?v=j9NZf9Wcodk', video.url)
        self.assertEqual('j9NZf9Wcodk', video.video_id)


    def test_add_invalid_vid_url(self):
        invalid_urls = [
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?awdawdawda',
            'https://www.youtube.com/watch?v=',
            'https://github.com',
        ]

        for vid_url in invalid_urls:
            new_vid = {
                'name': 'example',
                'url': vid_url,
                'notes': 'example'
            }

        url = reverse('add_video')
        response = self.client.post(url, new_vid)
        self.assertTemplateNotUsed('video_collection/add.html')
        messages = response.context['messages']
        message_text = [message.message for message in messages]

        self.assertIn('Invalid Youtube URL', message_text)
        self.assertIn('Enter valid data', message_text)

        video_count = Video.objects.count()
        self.assertEqual(0, video_count)



class TestVideoList(TestCase):
    
    def test_all_videos_displayed_in_correcr_ordeer(self):
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=124')
        v2 = Video.objects.create(name='abc', notes='example', url='https://www.youtube.com/watch?v=123')
        v3 = Video.objects.create(name='AAA', notes='example', url='https://www.youtube.com/watch?v=122')
        v4 = Video.objects.create(name='lmn', notes='example', url='https://www.youtube.com/watch?v=121')

        expected_order = [v3, v2, v4, v1]

        url = reverse('video_list')
        response = self.client.get(url)

        videos_in_template = list(response.context['videos'])

        self.assertEqual(videos_in_template, expected_order)

    def test_no_video_message(self):
        url = reverse('video_list')
        response = self.client.get(url)
        self.assertContains(response, 'No vids')
        self.assertEqual(0, len(response.context['videos']))

    def test_video_number_message_one_video(self):
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=124')
        url = reverse('video_list')
        response = self.client.get(url)

        self.assertContains(response, '1 video')
        self.assertNotContains(response, '1 videos')

    
    def test_video_number_message_more_than_one_video(self):
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=124')
        v2 = Video.objects.create(name='aaa', notes='example', url='https://www.youtube.com/watch?v=124332')
        url = reverse('video_list')
        response = self.client.get(url)

        self.assertContains(response, '2 videos')
       
        
        


class TestVideoSearch(TestCase):
    pass

class TestVideoModel(TestCase):
    
    def test_invalid_url_raises_validation_error(self):
        invalid_urls = [
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch/some',
            'https://www.youtube.com/watch?v=',
            'https://github.com',
        ]

        for vid_url in invalid_urls:
            with self.assertRaises(ValidationError):
                Video.objects.create(name='ex', url=vid_url, notes='ex')
        
        self.assertEqual(0, Video.objects.count())


    def test_dupliacte_video_raises_integrity_error(self):
        v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=124332')
        with self.assertRaises(IntegrityError):
            Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=124332')

