from hapiclient import hapi
from hapiplot import hapiplot

# http://localhost:8999/#server=DAS+2&dataset=Cassini/MAG/Magnitude&parameters=B_mag&start=2016-12-11T13:00:00&stop=2016-12-11T23:00&return=image&format=svg
# http://hapi-server.org/servers-dev/#server=FadenTemp&dataset=Iowa+City+Conditions&parameters=Temperature&start=2022-02-11T00:00:00.000Z&stop=2022-02-12T00:00:00.000Z&return=image&format=svg

all = False
bn = 3

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
