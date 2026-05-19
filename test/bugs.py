from hapiclient import hapi
from hapiplot import hapiplot


logging = True

bn = 7 # None => run all tests

opts  = {'logging': logging, 'usecache': False}
popts = {'useimagecache': False, 'logging': logging}

tests = {
    0: {
        "comment": "",
        "server": 'http://hapi-server.org/servers-dev/TestData3.1/hapi',
        "dataset": 'dataset1',
        "parameters": '',
        "start": '1970-01-01T00:00:00Z',
        "stop": '1970-01-01T00:00:10Z'
    },
    1: {
        "comment": "No data from 10-20s but still colored",
        "server": 'http://hapi-server.org/servers-dev/TestData2.0/hapi',
        "dataset": 'dataset1',
        "parameters": 'spectra',
        "start": '1970-01-01T00:00:01Z',
        "stop": '1970-01-01T00:00:30Z'
    },
    2: {
        "comment": "No data but still colored",
        "server": 'http://hapi-server.org/servers-dev/TestData2.0/hapi',
        "dataset": 'dataset1',
        "parameters": 'spectra',
        "start": '1970-01-01T00:00:11Z',
        "stop": '1970-01-01T00:00:12Z'
    },
    3: {
        "server": 'http://hapi-server.org/servers-dev/TestData3.0/hapi',
        "dataset": 'dataset1',
        "parameters": '',
        "start": '1970-01-01T00:00:00Z',
        "stop": '1970-01-01T00:02:00Z'
    },
    4: {
        "server": 'http://hapi-server.org/servers-dev/TestData3.0/hapi',
        "dataset": 'dataset1',
        "parameters": 'vector',
        "start": '1970-01-01T00:00:00Z',
        "stop": '1970-01-01T00:00:11Z'
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
    hapiplot(data, meta, **popts)

