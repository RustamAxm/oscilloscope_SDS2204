import sys
from typing import List, Tuple

import pyvisa


class SDS2204:
    def __init__(self):
        self.sds = self._sds_finder()
        self.sds.timeout = 2000
        print(self.sds.query('*IDN?'))
        self.sds.write('COMM_HEADER OFF')
        self.vdiv = self.sds.query('C1:VDIV?')
        self.ofst = self.sds.query('C1:OFST?')
        self.tdiv = self.sds.query('TDIV?')
        self.sara = self.get_sample_rate()

    def get_sample_rate(self) -> float:
        sara = self.sds.query('SARA?')
        sara_unit = {'G': 1e9, 'M': 1e6, 'k': 1e3}
        for unit in sara_unit.keys():
            if sara.find(unit) != -1:
                sara = sara.split(unit)
                sara = float(sara[0]) * sara_unit[unit]
                break
        return float(sara)

    def get_waveform(self, channel='C1') -> Tuple[List[float], List[float]]:
        recv = self._get_waveform_data(channel)
        volt_values = []
        adc_mid = 127
        adc_max = 255
        for data_recv in recv:
            if data_recv > adc_mid:
                data_recv -= adc_max
            else:
                pass
            volt_values.append(data_recv)

        time_value = []
        volt_grid = 25
        time_grid = 7
        for idx, volt_val in enumerate(volt_values):
            volt_values[idx] = volt_val / volt_grid * float(self.vdiv) - float(self.ofst)
            time_data = -(float(self.tdiv) * time_grid) + idx * (1 / self.sara)
            time_value.append(time_data)

        return time_value, volt_values

    def close_device(self):
        self.sds.close()

    def _run_trigger(self):
        self.sds.write('TRIG_MODE NORM')

    def _stop_trigger(self):
        self.sds.write('TRIG_MODE STOP')

    def _get_waveform_data(self, channel):
        self._run_trigger()
        self.sds.write('{}:WAVEFORM? DAT2'.format(channel))
        recv = list(self.sds.read_raw())
        self._stop_trigger()
        header = 16
        tail = len(recv) - 2
        return recv[header:tail]

    @staticmethod
    def _sds_finder():
        rm = pyvisa.ResourceManager('@py')
        list_rm = rm.list_resources('?*')
        if not list_rm:
            sys.exit(1)
        print(list_rm)

        for instr in list_rm:
            if 'SDS2' in instr:
                print('found device {}'.format(instr))
                try:
                    return rm.open_resource(instr)
                except ValueError:
                    print('device not found')
                    sys.exit(1)
