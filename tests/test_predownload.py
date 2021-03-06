import sys
import os
import os.path
import unittest
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from youtubedownloader.download import PreDownload, DownloadOptions

class PreDownloadTest(unittest.TestCase):

    def setUp(self):
        self.url = "https://www.youtube.com/watch?v=xSUQcQYgQCY"
        self.options = {
            "file_format": "mp3",
            "output_path": "/foo/bar/path1"
        }
        
        self.data = {
            "title": "Test",
            "uploader": "Me",
            "uploader_url": "/foo/bar/uploader",
            "thumbnail": "/foo/bar/path1",
            "duration": 250
        }
        
    def test_preDownloadEqOperator(self):
        predownload1 = PreDownload(self.url, self.options)
        predownload2 = PreDownload(self.url, self.options)
        self.assertEqual(predownload1, predownload2)
        
        options_with_different_output_path = self.options
        options_with_different_output_path.update({"output_path": "/foo/bar/path2"})
        predownload3 = PreDownload(self.url, options_with_different_output_path)
        self.assertNotEqual(predownload1, predownload3)
        
    def test_preDownloadPackAndUnpack(self):
        predownload = PreDownload(self.url, self.options)
        predownload.status = "ready"
        predownload.data.collect(self.data)
        
        packed = PreDownload.pack(predownload)
        self.assertTrue(isinstance(packed, dict))
        expected_keys = ["url", "destination_file", "status", "data", "options"]
        for key in packed.keys():
            self.assertTrue(key in expected_keys)
            
        unpacked = PreDownload.unpack(packed)
        self.assertEqual(unpacked.url, predownload.url)
        self.assertEqual(unpacked.destination_file, predownload.destination_file)
        self.assertEqual(unpacked.status, predownload.status)
        self.assertEqual(unpacked.options, DownloadOptions(self.options))
        self.assertEqual(unpacked.data._title, predownload.data._title)
        self.assertEqual(unpacked.data._uploader, predownload.data._uploader)
        self.assertEqual(unpacked.data._thumbnail, predownload.data._thumbnail)
        self.assertEqual(unpacked.data._duration, predownload.data._duration)

if __name__ == "__main__":
    unittest.main()
