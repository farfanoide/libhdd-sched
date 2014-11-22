import unittest
from lib.simulation import Hdd


class TestHdd(unittest.TestCase):

    data = {
        'valid': {
            'name': 'protodisk',
            'tracks': 512,
            'rpm': 5400,
            'seek_time': 500
        },
        'strings': {
            'name': 'protodisk',
            'tracks': '512',
            'rpm': '5400',
            'seek_time': '500'
        }
    }

    def test_hdd_data_types(self):
        hdd = Hdd(self.data['strings'])
        self.assertIsInstance(hdd.tracks, int)

if __name__ == '__main__':
    unittest.main()
