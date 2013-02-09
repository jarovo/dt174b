import unittest
from itertools import islice

from dt174b import dt174b

class TestSettingPacket(unittest.TestCase):
    def setUp(self):
        self.def_data = {
                'year': 2013,
                'month': 2,
                'day': 5,
                'hour': 9,
                'min': 5,
                'sec': 24,
                'rec_int': 10,
                'alm_int': 10,
                'smpl_int': 1,
                'auto': False,
                'temp_high': 40.5,
                'temp_low': 5.5,
                'hum_high': 90.5,
                'hum_low': 30.5,
                'pressure_high': 1100,
                'pressure_low': 700,
                'alt': 0,
                'samples': 10000
        }

        self.edge_data = {
                'year': 2013,
                'month': 2,
                'day': 5,
                'hour': 9,
                'min': 5,
                'sec': 24,
                'rec_int': None,
                'alm_int': None,
                'smpl_int': 17*60 + 59,
                'auto': True,
                'temp_high': 70,
                'temp_low': -40,
                'hum_high': 100,
                'hum_low': 0,
                'pressure_high': 1100,
                'pressure_low': 700,
                'alt': -9999,
                'samples': 10
        }

    def test_default(self):
        packet = dt174b.SettingsPacket(**self.def_data)
        expected = (
            '18 05 09 '     # time
            '05 02 07dd '   # date
            'ff ff ff '     # unknown
            '0a 0a '        # signaling rates
            '0001 00 '      # sampling rate, trig source
            '0fd2 0226 '    # temperature
            '0389 0131 '    # humidity
            '0364 f3c4 '    # pressure
            '5a '           # unknown
            '0000 2710 '    # alt, samples
        )
        packed_packet = packet.pack().encode('hex')
        i = iter(packed_packet)
        for ex in expected.split():
            self.assertEquals(ex, ''.join(take(len(ex), i)))

    def test_edge_vals(self):
        packet = dt174b.SettingsPacket(**self.edge_data)
        expected = (
            '18 05 09 '     # time
            '05 02 07dd '   # date
            'ff ff ff '     # uknown
            'ff ff '        # signaling rates
            '0437 01 '      # sampling rate, trig source
            '1b58 f060 '    # temp
            '03e8 0000 '    # humidity
            '0364 f3c4 '    # pressure
            '5a '           # unknown
            'd8f1 000a '    # alt, samples
        )

        packed_packet = packet.pack().encode('hex')
        i = iter(packed_packet)
        for ex in expected.split():
            self.assertEquals(ex, ''.join(take(len(ex), i)))


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

