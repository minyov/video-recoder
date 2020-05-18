from django.test import TransactionTestCase

from apps.video import models, tasks, enums


class TestVideoModel(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_name = '0f9a2669f1957bb2de310de54d4aeea8'
        cls.file_ext = 'mp4'

        cls.url_video = models.Video.objects.create(
            url='https://test.ru/video.mp4',
        )

        cls.file_video = models.Video.objects.create(
            file=f'/originals/{cls.file_name}.{cls.file_ext}',
        )

        cls.processed_video = models.Video.objects.create(
            url='https://test.ru/video.mp4',
            file=f'/originals/{cls.file_name}.{cls.file_ext}',
            preview=f'/previews/{cls.file_name}.jpg',
            mp4=f'/mp4/{cls.file_name}.mp4',
            webm=f'/mp4/{cls.file_name}.webm',
        )

    def test_count(self):
        self.assertEquals(models.Video.objects.count(), 3)

    def test_url_video(self):
        self.assertFalse(self.url_video.processed)

    def test_file_video(self):
        self.assertFalse(self.file_video.processed)

    def test_processed_video_properties(self):
        self.assertTrue(self.processed_video.processed)

        self.assertEquals(self.processed_video.full_file_name, f'{self.file_name}.{self.file_ext}')
        self.assertEquals(self.processed_video.file_name, self.file_name)
        self.assertEquals(self.processed_video.file_ext, self.file_ext)
        self.assertEquals(str(self.processed_video), str(self.processed_video.id))

    def test_upload_to(self):
        dir_name = 'dir'
        file_ext = 'mp4'

        upload_to = models.UploadTo(dir_name)
        file_path = upload_to(self.url_video, f'filename.{file_ext}')

        self.assertIn(dir_name + '/', file_path)
        self.assertIn('.' + file_ext, file_path)

        upload_to = models.UploadTo(dir_name)
        file_path = upload_to(self.file_video, f'filename.{file_ext}')
        original_file_path = self.file_video.file.name

        self.assertEquals('/' + file_path, original_file_path.replace('originals', dir_name))


class TestDownloadVideo(TransactionTestCase):
    def setUp(self):
        url = 'http://mirrors.standaloneinstaller.com/video-sample/small.3gp'
        wrong_mime_type_url = 'http://mirrors.standaloneinstaller.com/video-sample/grb_2.wmv'

        self.url_video = models.Video.objects.create(
            url=url,
        )

        self.wrong_mime_type_video = models.Video.objects.create(
            url=wrong_mime_type_url,
        )

    def test_download(self):
        self.assertFalse(self.url_video.file)
        tasks.download_video_file(video_id=self.url_video.id)
        self.url_video.refresh_from_db()
        self.assertTrue(self.url_video.file)

    def test_download_wrong_mime_type(self):
        self.assertFalse(self.wrong_mime_type_video.file)
        tasks.download_video_file(video_id=self.url_video.id)
        self.wrong_mime_type_video.refresh_from_db()
        self.assertFalse(self.wrong_mime_type_video.file)


class TestRecodeVideo(TransactionTestCase):
    def setUp(self):
        url = 'http://mirrors.standaloneinstaller.com/video-sample/small.mp4'

        self.url_video = models.Video.objects.create(
            url=url,
        )
        tasks.download_video_file(video_id=self.url_video.id)
        self.url_video.refresh_from_db()

    def test_recode_to_mp4(self):
        self.assertTrue(self.url_video.file)

        self.assertFalse(self.url_video.mp4)
        tasks.recode_video(video_id=self.url_video.id, ext=enums.VideoMimeTypeEnum.MP4.value)
        self.url_video.refresh_from_db()
        self.assertTrue(self.url_video.mp4)

    def test_recode_to_webm(self):
        self.assertTrue(self.url_video.file)

        self.assertFalse(self.url_video.webm)
        tasks.recode_video(video_id=self.url_video.id, ext=enums.VideoMimeTypeEnum.WEBM.value)
        self.url_video.refresh_from_db()
        self.assertTrue(self.url_video.webm)


class TestCreatePreview(TransactionTestCase):
    def setUp(self):
        url = 'http://mirrors.standaloneinstaller.com/video-sample/small.mp4'

        self.url_video = models.Video.objects.create(
            url=url,
        )
        tasks.download_video_file(video_id=self.url_video.id)
        self.url_video.refresh_from_db()

    def test_create_preview(self):
        self.assertTrue(self.url_video.file)

        self.assertFalse(self.url_video.preview)
        tasks.create_preview(video_id=self.url_video.id)
        self.url_video.refresh_from_db()
        self.assertTrue(self.url_video.preview)
