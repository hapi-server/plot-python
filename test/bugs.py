from hapiclient import hapi
from hapiplot import hapiplot

# http://localhost:8999/#server=DAS+2&dataset=Cassini/MAG/Magnitude&parameters=B_mag&start=2016-12-11T13:00:00&stop=2016-12-11T23:00&return=image&format=svg
# http://hapi-server.org/servers-dev/#server=FadenTemp&dataset=Iowa+City+Conditions&parameters=Temperature&start=2022-02-11T00:00:00.000Z&stop=2022-02-12T00:00:00.000Z&return=image&format=svg

all = False
bn = 3

if bn == 0 or all == True:
    server     = 'http://hapi-server.org/servers-dev/TestData3.1/hapi'
    dataset    = 'dataset1'
    parameter  = ''
    start      = '1970-01-01T00:00:00Z'
    stop       = '1970-01-01T00:00:10Z'

    opts       = {'logging': True, 'usecache': False}

    meta = hapi(server, dataset, **opts)

    for i in range(0,len(meta['parameters'])):
        parameter  = meta['parameters'][i]['name']
        print("test_hapiplot(): Plotting " + parameter)
        data, metax = hapi(server, dataset, parameter, start, stop, **opts)

        popts = {'useimagecache': False, 'logging': True}

        metap = hapiplot(data, metax, **popts)

if bn == 1 or all == True:
    # No data from 10-20 but still colored
    server     = 'http://hapi-server.org/servers-dev/TestData2.0/hapi'
    dataset    = 'dataset1'
    parameter  = 'spectra'
    start      = '1970-01-01T00:00:01Z'
    stop       = '1970-01-01T00:00:30Z'
    opts       = {'logging': True, 'usecache': True}

    data, meta = hapi(server, dataset, parameter, start, stop, **opts)

    popts      = {'logging': True, 'returnimage': False, 'usecache': False}
    hapiplot(data, meta, **popts)

if bn == 2 or all == True:
    # Should be "no data"
    server     = 'http://hapi-server.org/servers-dev/TestData2.0/hapi'
    dataset    = 'dataset1'
    parameter  = 'spectra'
    start      = '1970-01-01T00:00:11Z'
    stop       = '1970-01-01T00:00:12Z'
    opts       = {'logging': True, 'usecache': False}

    data, meta = hapi(server, dataset, parameter, start, stop, **opts)

    popts      = {'logging': True, 'returnimage': False, 'usecache': False}
    hapiplot(data, meta, **popts)

if bn == 3 or all == True:

    logging = True
    server     = 'http://hapi-server.org/servers/TestData3.0/hapi'
    dataset    = 'dataset1'
    parameters = ''
    start      = '1970-01-01Z'
    stop       = '1970-01-01T00:02:00Z'
    opts       = {'logging': logging, 'usecache': False}

    data, metax = hapi(server, dataset, parameters, start, stop, **opts)

    popts = {'useimagecache': False, 'logging': logging}

    hapiplot(data, metax, **popts)

if bn == 4 or all == True:

    logging = True
    server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
    dataset    = 'dataset1'
    parameters = 'vector'
    start      = '1970-01-01Z'
    stop       = '1970-01-01T00:00:11Z'
    opts       = {'logging': logging, 'usecache': False}

    data, metax = hapi(server, dataset, parameters, start, stop, **opts)

    popts = {'useimagecache': False, 'logging': logging}

    hapiplot(data, metax, **popts)
