from hapiclient import hapi
from hapiplot import hapiplot
import os


logging = False

bn = 22 
#bn = None # None => run all tests

opts  = {'logging': logging, 'usecache': False}
popts = {'useimagecache': False, 'logging': logging, 'returnimage': True}

tests = {
    0: {
        "comment": "",
        "server": 'http://hapi-server.org/servers/TestData3.1/hapi',
        "dataset": 'dataset1',
        "parameters": '',
        "start": '1970-01-01T00:00:00Z',
        "stop": '1970-01-01T00:00:10Z'
    },
    1: {
        "comment": "No data from 10-20s but still colored",
        "server": 'http://hapi-server.org/servers/TestData2.0/hapi',
        "dataset": 'dataset1',
        "parameters": 'spectra',
        "start": '1970-01-01T00:00:01Z',
        "stop": '1970-01-01T00:00:30Z'
    },
    2: {
        "comment": "No data but still colored",
        "server": 'http://hapi-server.org/servers/TestData2.0/hapi',
        "dataset": 'dataset1',
        "parameters": 'spectra',
        "start": '1970-01-01T00:00:11Z',
        "stop": '1970-01-01T00:00:12Z'
    },
    3: {
        "server": 'http://hapi-server.org/servers/TestData3.0/hapi',
        "dataset": 'dataset1',
        "parameters": '',
        "start": '1970-01-01T00:00:00Z',
        "stop": '1970-01-01T00:02:00Z'
    },
    4: {
        "comment": "no data but",
        "server": 'http://hapi-server.org/servers/TestData2.0/hapi',
        "dataset": 'dataset1',
        "parameters": 'vector',
        "start": '1970-01-01T00:00:11Z',
        "stop": '1970-01-01T00:00:12Z'
    },
    5: {
        "server": 'https://cdaweb.gsfc.nasa.gov/hapi',
        "dataset": 'THE_L2_FGM@0',
        "parameters": 'the_fgs_gsm',
        "start": '2024-08-11T00:00:00Z',
        "stop": '2024-08-12T00:00:00.000Z'
    },
    6: {
        "server": 'https://supermag.jhuapl.edu/hapi',
        "dataset": 'indices_all',
        "parameters": 'SMUdstid',
        "start": '2018-01-18T00:00Z',
        "stop": '2018-01-19T01:00Z'
    },
    7: {
        "server": 'https://jfaden.net/HapiServerDemo/hapi',
        "dataset": 'Iowa City Conditions',
        "parameters": 'Temperature',
        "start": '2022-02-11T00:00:00.000Z',
        "stop": '2022-02-12T00:00:00.000Z'
    },
    8: {
        'server': 'https://planet.physics.uiowa.edu/das/das2Server/hapi',
        'dataset': 'Cassini/MAG/Magnitude',
        'parameters': '',
        'start': '2016-12-11T13:00:00',
        'stop': '2016-12-11T23:00'
    },
    9: {
        'server': 'https://www.ncei.noaa.gov/cloud-access/space-weather-portal/api/v1/hapi',
        'dataset': 'CCOR1_1A',
        'parameters': 'ISPREG1',
        'start': '2025-02-01T00:00:20.745Z',
        'stop': '2025-02-02T00:00:20.745Z'
    },
    10: {
        'server': 'https://iswa.gsfc.nasa.gov/hapi',
        'dataset': 'GFZ_Indices_P3H',
        'parameters': 'Kp_observed',
        'start': '1932-01-01T00:00:00Z',
        'stop': '1932-01-03T00:00:00.000Z'
    },
    11: {
        "comment": "matrix parameter",
        "server": 'http://hapi-server.org/servers/TestData2.1/hapi',
        "dataset": 'dataset1',
        "parameters": 'matrix',
        "start": '1970-01-01Z',
        "stop": '1970-01-01T00:00:11Z'
    },
    12: {
        "comment": "All NaNs",
        "server": 'https://cdaweb.gsfc.nasa.gov/hapi',
        "dataset": 'AC_H0_MFI',
        "parameters": 'Magnitude,BGSEc',
        "start": '1997-12-10T00:00:00',
        "stop": '1997-12-11T10:00:00'
    },
    13: {
        "comment": "Time-only parameter",
        "server": 'http://hapi-server.org/servers/SSCWeb/hapi',
        "dataset": 'rbspa',
        "parameters": 'Time',
        "start": '2012-08-31T00:00:00.000Z',
        "stop": '2012-08-31T23:59:59.999Z'
    },
    14: {
        "server": 'http://hapi-server.org/servers/SSCWeb/hapi',
        "dataset": 'ace',
        "parameters": 'Y_TOD',
        "start": '1997-09-15T00:00:00.000Z',
        "stop": '1997-09-25T23:59:59.999Z'
    },
    15: {
        "comment": "No data in interval",
        "server": 'https://vires.services/hapi',
        "dataset": 'SW_OPER_MAGB_LR_1B',
        "parameters": 'B_VFM',
        "start": '2013-11-26T16:00:00.000Z',
        "stop": '2013-11-26T16:59:59.999Z'
    },
    16: {
        "comment": "Stop time missing trailing Z",
        "server": 'http://planet.physics.uiowa.edu/das/das2Server/hapi',
        "dataset": 'Cassini/MAG/Magnitude',
        "parameters": 'B_mag',
        "start": '2016-12-11T13:00:00Z',
        "stop": '2016-12-11T23:00'
    },
    17: {
        "comment": "size=[2,3] two sets of 3-component vectors. Previously interpretation of size was backwards. Here size=[2,3] which means two sets of 3-component vectors.",
        "server": 'http://hapi-server.org/servers/TestData2.0/hapi',
        "dataset": 'dataset1',
        "parameters": 'vectormulti',
        "start": '1970-01-01Z',
        "stop": '1970-01-01T00:00:11Z'
    },
    18: {
        "server": 'https://jfaden.net/HapiServerDemo/hapi',
        "dataset": 'atticTemperature',
        "parameters": 'Temperature',
        "start": '2022-03-06T00:00:00.000Z',
        "stop": '2022-03-07T00:00:00.000Z'
    },
    19: {
        "server": 'https://cdaweb.gsfc.nasa.gov/hapi',
        "dataset": 'GOES13_EPS-MAGED_1MIN',
        "parameters": 'dtc_cor_eflux_stack9',
        "start": '2010-06-02T00:00:00Z',
        "stop": '2010-06-03T00:00:00.000Z'
    },
    20: {
        "comment": "Scalar out of range - no data",
        "server": 'http://hapi-server.org/servers/TestData2.0/hapi',
        "dataset": 'dataset1',
        "parameters": 'scalar',
        "start": '1970-01-01T00:00:11Z',
        "stop": '1970-01-01T00:00:12Z'
    },
    21: {
        "comment": "All parameters - no data",
        "server": 'http://hapi-server.org/servers/TestData2.0/hapi',
        "dataset": 'dataset1',
        "parameters": '',
        "start": '1970-01-01T00:00:11Z',
        "stop": '1970-01-01T00:00:12Z'
    },
    22: {
        "comment": "All parameters - one valid point",
        "server": 'http://hapi-server.org/servers/TestData2.0/hapi',
        "dataset": 'dataset1',
        "parameters": '',
        "start": '1970-01-01T00:00:09Z',
        "stop": '1970-01-01T00:00:11Z'
    }
}

for tn in tests.keys():
    if bn is not None and tn != bn:
        continue

    test = tests[tn]
    if 'comment' in test:
        print(f"Running test {tn} - {test['comment']}")
    else:
        print(f"Running test {tn}")

    server     = test['server']
    dataset    = test['dataset']
    parameters = test['parameters']
    start      = test['start']
    stop       = test['stop']

    data, meta = hapi(server, dataset, parameters, start, stop, **opts)
    meta = hapiplot(data, meta, **popts)
    os.makedirs('./bugs', exist_ok=True)
    figs = [p['hapiplot']['figure'] for p in meta["parameters"]
            if 'hapiplot' in p and 'figure' in p['hapiplot']]
    for j, fig in enumerate(figs):
        fname = f'./bugs/bugs_{tn:02d}.png' if len(figs) == 1 else f'./bugs/bugs_{tn:02d}_{j+1:02d}.png'
        fig.savefig(fname, bbox_inches='tight')
        print(f"  Saved {fname}")
