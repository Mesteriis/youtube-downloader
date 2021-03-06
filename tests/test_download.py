import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader.download import Download, PreDownload


class DownloadTest(unittest.TestCase):
    def setUp(self):
        self.url = "https://www.youtube.com/watch?v=_mVW8tgGY_w"
        
        self.options = {
            "file_format": "mp3",
            "output_path": "/foo/bar/path"
        }
        
        self.data = {
            "title": "test",
            "uploader": "test1",
            "uploader_url": "/foo/bar/uploader",
            "thumbnail": "None",
            "duration": 60,
        }
            
    def test_downloadEqOperator(self):
        download1 = Download(self.url, self.options, self.data)
        download2 = Download(self.url, self.options, self.data)
        self.assertEqual(download1, download2)
        
        options_with_different_file_format = self.options
        options_with_different_file_format.update({"file_format": "mp4"})
        download3 = Download(self.url, options_with_different_file_format, self.data)
        self.assertNotEqual(download1, download3)
        
    def test_downloadPackAndUnPack(self):
        download = Download(self.url, self.options, self.data)
        
        packed = Download.pack(download)
        self.assertTrue(isinstance(packed, dict))
        
        expected_keys = ["url", "destination_file", "options", "data", "progress"]
        for key in packed.keys():
            self.assertTrue(key in expected_keys)
            
        unpacked = Download.unpack(packed)
        self.assertEqual(unpacked.url, download.url)
        self.assertEqual(unpacked.options, download.options)
        self.assertEqual(unpacked.data._title, download.data._title)
        self.assertEqual(unpacked.data._uploader, download.data._uploader)
        self.assertEqual(unpacked.data._uploader_url, download.data._uploader_url)
        self.assertEqual(unpacked.data._thumbnail, download.data._thumbnail)
        self.assertEqual(unpacked.data._duration, download.data._duration)
        
                    
    def test_downloadInitializesByPreDownload(self):
        data = {
            "title": "test1",
            "uploader": "admin",
            "uploader_url": "/foo/bar/uploader",
            "thumbnail": "None",
            "duration": 60
        }
        
        predownload = PreDownload(self.url, self.options)
        predownload.data.collect(data)
        predownload.update()
        
        download = Download.fromPreDownload(predownload)
        self.assertEqual(download.url, predownload.url)
        self.assertEqual(download.destination_file, predownload.destination_file)
        self.assertEqual(download.options, predownload.options)
        self.assertEqual(download.data._title, predownload.data._title)
        self.assertEqual(download.data._uploader, predownload.data._uploader)
        self.assertEqual(download.data._thumbnail, predownload.data._thumbnail)
        self.assertEqual(download.data._duration, predownload.data._duration)
        

if __name__ == "__main__":
    unittest.main()
