# simulator_mosaik.py

import logging
import mosaik_api
import batterysim.model

logger = logging.getLogger('batterysim')

META = {
    'models': {
        'BatteryModel': {
            'public': True,
            'params': [
                'sim_start',
                'battery_file',
                'grid_name',
                ],
            'attrs': [],
        },
        'Battery': {
            'public': False,
            'params': [],
            'attrs': [
                'P_bat',
                'soc',
                'mode',
                'num',
                'node_id',
            ],
        },
    },
}


def eid(hid):
    return 'Battery_%s' % hid


class BatterySim(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)

        self.model = None
        self.batteries_by_eid = {}
        self.pos_loads = None
        self._file_cache = {}
        self._offset = 0
        self._cacje = {}

    def init(self, sid):
        return self.meta

    def create(self, num, model, sim_start, battery_file, grid_name):
        if num != 1 or self.model:
            raise ValueError('Can only create one set of batteries.')

        logger.info('Creating batteries for %s from "%s"' % (grid_name,
                                                             battery_file))
        bf = open(battery_file, 'rt')
        self.model = batterysim.model.BatteryModel(bf, grid_name)
        self.batteries_by_eid = {
            eid(i): battery
            for i, battery in enumerate(self.model.batteries)
        }

        self._offset = self.model.get_delta(sim_start)

        return [{
            'eid': 'batt_0',
            'type': 'BatteryModel',
            'rel': [],
            'children': [{
                'eid': eid(i),
                'type': 'Battery',
                'rel': []
            } for i, _ in enumerate(self.model.batteries)],
        }]

    def step(self, time, inputs):
        deltas = {}
        for eid, attrs in inputs.items():
            for attr, values in attrs.items():
                new_delta = sum(values.values())
                deltas[eid] = new_delta

        # Perform simulation step
        self.model.step(deltas)

        return time + self.model.resolution

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            data[eid] = {}
            for attr in attrs:
                if attr == 'soc':
                    val = self.batteries_by_eid[eid]['object'].soc
                if attr == 'P_batt':
                    val = self.batteries_by_eid[eid]['object'].P_batt
                if attr == 'delta':
                    val = self.batteries_by_eid[eid]['object'].delta
                data[eid][attr] = val
        return data


def main():
    return mosaik_api.start_simulation(BatterySim(), 'Battery Simulation')
