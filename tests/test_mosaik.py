# test file for baterysim.mosaik.py

from os.path import dirname, join
import unittest
from batterysim import mosaik


DATA_FILE = join(dirname(__file__), 'data', 'test.data')


class TestBatterySim(unittest.TestCase):
    def setUp(self):
        self.sim = mosaik.BatterySim()
        self.meta = self.sim.init('sid')
        self.inputs = {
                'battery_0': {
                    'power_rating': {
                        'agent_0': 0
                        },
                    },
                'battery_1': {
                    'power_rating': {
                        'agent_1': 0.3
                        },
                    },
                }

    def test_init(self):
        entities = self.sim.create(
            1,
            'BatteryModel',
            sim_start='2014-01-01 00:00:00',
            battery_file=DATA_FILE,
            grid_name='grid_test')

        self.assertEqual(entities, [
            {
                'eid': 'batt_0',
                'type': 'BatteryModel',
                'rel': [],
                'children': [{
                    'eid': 'Battery_%s' % i,
                    'type': 'Battery',
                    'rel': []
                } for i in range(3)]
            },
        ])

    def test_init_error(self):
        # Create to many instances
        self.assertRaises(ValueError, lambda: self.sim.create(
            2,
            'BatteryModel',
            sim_start='2014-01-01 00:00:00',
            battery_file=DATA_FILE,
            grid_name='grid_test'))

        # Call create() twice
        self.sim.create(
            1,
            'BatteryModel',
            sim_start='2014-01-01 00:00:00',
            battery_file=DATA_FILE,
            grid_name='grid_test')
        self.assertRaises(ValueError, lambda: self.sim.create(
            1,
            'BatteryModel',
            sim_start='2014-01-01 00:00:00',
            battery_file=DATA_FILE,
            grid_name='grid_test'))

    def test_create(self):
        self.assertEqual(
            list(sorted(self.meta['models'].keys())),
            ['Battery', 'BatteryModel'])

        entities = self.sim.create(
            1,
            'BatteryModel',
            sim_start='2014-01-01 00:00:00',
            battery_file=join(dirname(__file__), 'data', 'test.data'),
            grid_name='grid_test')
        self.assertEqual(entities, [
            {
                'eid': 'batt_0',
                'type': 'BatteryModel',
                'rel': [],
                'children': [
                    {
                        'eid': 'Battery_0',
                        'type': 'Battery',
                        'rel': []
                    },
                    {
                        'eid': 'Battery_1',
                        'type': 'Battery',
                        'rel': []
                    },
                    {
                        'eid': 'Battery_2',
                        'type': 'Battery',
                        'rel': []
                    },
                ]
            },
        ])

    def test_step(self):
        self.sim.create(
            1,
            'BatteryModel',
            sim_start='2014-01-01 00:00:00',
            battery_file=join(dirname(__file__), 'data', 'test.data'),
            grid_name='grid_test')

        self.assertEqual(self.sim.step(0, self.inputs), 1)

    def test_get_data(self):
        self.sim.create(
            1,
            'BatteryModel',
            sim_start='2014-01-01 00:00:00',
            battery_file=join(dirname(__file__), 'data', 'test.data'),
            grid_name='grid_test')

        data = self.sim.get_data({
            'Battery_0': ['charge'],
            'Battery_1': ['charge']
        })
        self.assertEqual(data, {
            'Battery_0': {
                'charge': 0
            },
            'Battery_1': {
                'charge': 0.1
            },
        })

        self.sim.step(1, self.inputs)
        data = self.sim.get_data({
            'Battery_0': ['power_rating'],
            'Battery_1': ['power_rating']
        })
        self.assertEqual(data, {
            'Battery_0': {
                'power_rating': 0
            },
            'Battery_1': {
                'power_rating': 0
            },
        })
