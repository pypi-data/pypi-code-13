import unittest
from path_list import PathsList

class PathsListTest(unittest.TestCase):
    def test_one_step(self):
        test_arr = """
                global
                media
                    video
                        video-sources
                        picture-sources
                        vector-sources
                        audio-sources
                        font-sources
                        document-sources
                    audio
                        music&soundtrack
                        sfx
                        vo
            """.split("\n")
        paths_list = PathsList(test_arr)
        self.assertEqual(
            paths_list,
            [
                'global',
                'media',
                'media/video',
                'media/video/video-sources',
                'media/video/picture-sources',
                'media/video/vector-sources',
                'media/video/audio-sources',
                'media/video/font-sources',
                'media/video/document-sources',
                'media/audio',
                'media/audio/music&soundtrack',
                'media/audio/sfx',
                'media/audio/vo'
            ]
        )
