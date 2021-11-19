from django.test import TestCase
from django.urls import reverse
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



class TestVideoList(TestCase):
    pass

class TestVideoSearch(TestCase):
    pass

class TestVideoModel(TestCase):
    pass