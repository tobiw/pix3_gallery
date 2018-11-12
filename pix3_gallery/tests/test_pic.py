import os
import subprocess
from glob import glob
from nose.tools import assert_equal
from ..pic import Pic


TESTALBUM = 'album/testalbum'
TESTIMG = 'testimg.png'


class TestPic:
    def teardown(self):
        try:
            os.remove(TESTIMG)
        except OSError:
            pass

    def test_single_seperators(self):
        assert_equal(str(Pic('test1/test2.png')._path), 'test1/test2.png')

    def test_multiple_seperators(self):
        assert_equal(str(Pic('test1//test2.png')._path), 'test1/test2.png')

    # def test_album_dir_split(self):
        # assert_equal(str(Pic('test 111/test 222/test3.png').album_path), 'test 111/test 222')

    def test_filename_split(self):
        assert_equal(Pic('test 111/test 222/test3.png').filename, 'test3.png')

    def test_fake_image(self):
        subprocess.check_call(['convert', '-size', '800x600', 'xc:red', TESTIMG])
        assert_equal(Pic(TESTIMG).size, (800, 600))

    def test_cached_size(self):
        subprocess.check_call(['convert', '-size', '800x600', 'xc:red', TESTIMG])
        pic = Pic(TESTIMG)
        assert_equal(pic.size, (800, 600))
        os.remove(TESTIMG)
        assert_equal(pic.size, (800, 600))

    def test_resized_pic_path(self):
        pic = Pic(os.path.join(TESTALBUM, TESTIMG))
        expected = os.path.join(TESTALBUM, '.xzy_' + TESTIMG)
        assert_equal(str(pic._get_resized_pic_path('xzy')), expected)


class TestPicMeta:
    @classmethod
    def setupAll(cls):
        os.makedirs(TESTALBUM)
        with open(os.path.join(TESTALBUM, '.meta'), 'w') as f:
            f.write('<album description>\n</album description>\n')
            f.write(TESTIMG + ' = test_comment 123')

    @classmethod
    def teardownAll(cls):
        os.remove(os.path.join(TESTALBUM, '.meta'))
        os.removedirs(TESTALBUM)

    def setup(self):
        self.pic = Pic(os.path.join(TESTALBUM, TESTIMG))

    def test_comment(self):
        comment = self.pic.comment
        assert comment == 'test_comment 123', comment


def _get_image_size(img):
    text = subprocess.check_output(['identify', img]).decode()
    return tuple([int(x) for x in text.split()[2].split('x')])


class TestPicResized:
    def setup(self):
        subprocess.check_call(['convert', '-size', '800x600', 'xc:red', TESTIMG])
        Pic._config = {}
        self.pic = Pic(TESTIMG)
        self.pic.generate_resized()

    def teardown(self):
        del self.pic
        os.remove(TESTIMG)
        for f in glob('.*_' + TESTIMG):
            os.remove(f)

    def test_thumb(self):
        assert_equal(self.pic.thumbnail_path, '.thumb_' + TESTIMG)
        assert os.path.exists(self.pic.thumbnail_path), '{!s} does not exist'.format(self.pic.thumbnail_path)

    def test_web(self):
        assert_equal(self.pic.web_path, '.web_' + TESTIMG)
        assert os.path.exists(self.pic.web_path), '{!s} does not exist'.format(self.pic.web_path)

    def test_try_recreate_resized(self):
        for i in range(2):
            self.pic.generate_resized()
            assert_equal(self.pic.web_path, '.web_' + TESTIMG)

    # def test_try_recreate_cropped(self):
    #     Pic._config['crop-thumbnails'] = True
    #     for i in range(2):
    #         assert_equal(self.pic.thumbnail_path, '.thumb_' + TESTIMG)

    # def test_thumb_size_resized(self):
    #     self.pic.thumbnail_path
    #     assert_equal(_get_image_size('.thumb_' + TESTIMG), (80, 60))

    # def test_thumb_size_cropped(self):
    #     Pic._config['crop-thumbnails'] = True
    #     self.pic.thumbnail_path
    #     assert_equal(_get_image_size('.thumb_' + TESTIMG), (80, 80))

    def test_web_size(self):
        assert_equal(self.pic.size, (500, 375))

    # def test_thumb_size_resized_custom(self):
    #     expected_size = (160, 120)
    #     Pic._config['thumbnail-size'] = expected_size
    #     self.pic.thumbnail_path
    #     assert_equal(_get_image_size('.thumb_' + TESTIMG), expected_size)

    # def test_thumb_size_cropped_custom(self):
    #     Pic._config['crop-thumbnails'] = True
    #     expected_size = 120
    #     Pic._config['thumbnail-size'] = expected_size
    #     self.pic.thumbnail_path
    #     assert_equal(_get_image_size('.thumb_' + TESTIMG), (expected_size, expected_size))

    # def test_web_size_custom(self):
    #     expected_size = (640, 480)
    #     Pic._config['web-size'] = expected_size
    #     self.pic.web_path
    #     assert_equal(_get_image_size('.web_' + TESTIMG), expected_size)
