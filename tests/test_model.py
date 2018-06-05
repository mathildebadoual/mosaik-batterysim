from os.path import dirname, join

import arrow
import unittest

from batterysim.model import BatteryModel


data_file = join(dirname(__file__), 'data', 'test.data')


class TestHouseModel(unittest.TestCase):
    def setUp(self):
        self.bm = BatteryModel(open(data_file), 'grid_test')

    def test_batterymodel_init(self):
        self.assertEqual(self.bm.start, arrow.get('2014-01-01'))
        self.assertEqual(self.bm.unit, 'W')
        self.assertEqual(self.bm.num_batteries, 3)

        # soc_init
        self.assertEqual(self.bm.attrs['soc_init'][2], 0.5)

    def test_batterymodel_get(self):
        self.assertEqual(self.bm.get(10)[2], 0.5)

    def test_batterymodel_get_delta(self):
        date = '2014-01-03 01:00:00'
        delta = 2940
        minutes = self.bm.get_delta(date)
        self.assertEqual(minutes, delta)

    def test_batterymodel_get_delta_error(self):
        self.assertRaises(ValueError,
                          lambda: self.bm.get_delta('2013-01-01 01:00:00'))
