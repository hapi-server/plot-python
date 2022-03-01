from hapiclient import hapi
from hapiplot import hapiplot

if True:
    server     = 'http://hapi-server.org/servers/SSCWeb/hapi'
    dataset    = 'ace'
    parameter  = 'Y_TOD'
    start      = '1997-09-15T00:00:00.000Z'
    stop       = '1997-09-25T23:59:59.999Z'

    opts       = {'logging': True, 'usecache': False}

    data, meta = hapi(server, dataset, parameter, start, stop, **opts)

    popts = {'logging': True,
             'returnimage': True,
             'useimagecache': False,
             'saveimage': True,
             'rcParams': {'savefig.transparent': True,
                          'savefig.format': 'svg'
                          }
             }

    meta = hapiplot(data, meta, **popts)

    from IPython.display import Image
    Image(data = meta['parameters'][1]['hapiplot']['image'])

if False:
    server     = 'https://vires.services/hapi'
    dataset    = 'SW_OPER_MAGB_LR_1B'
    parameter  = 'B_VFM'
    #start      = '2013-11-25T16:00:00.000Z'
    #stop       = '2013-11-25T16:59:59.999Z'
    start      = '2013-11-26T16:00:00.000Z'
    stop       = '2013-11-26T16:59:59.999Z'

    opts       = {'logging': True, 'usecache': True}

    data, meta = hapi(server, dataset, parameter, start, stop, **opts)

    popts      = {'logging': True, 'returnimage': False, 'usecache': False}
    hapiplot(data, meta, **popts)

if False:
    server     = 'http://planet.physics.uiowa.edu/das/das2Server/hapi'
    dataset    = 'Cassini/MAG/Magnitude'
    #parameter  = 'spectramulti'
    #parameter  = 'transformmulti'
    parameter  = 'B_mag'
    start      = '2016-12-11T13:00:00Z'
    stop       = '2016-12-11T23:00'
    opts       = {'logging': True, 'usecache': False}

    data, meta = hapi(server, dataset, parameter, start, stop, **opts)

    popts      = {'logging': True, 'returnimage': False, 'usecache': False}
    hapiplot(data, meta, **popts)

if False:
    server     = 'http://hapi-server.org/servers-dev/TestData2.0/hapi'
    dataset    = 'dataset1'
    #parameter  = 'spectramulti'
    #parameter  = 'transformmulti'
    parameter  = 'vectormulti'
    start      = '1970-01-01Z'
    stop       = '1970-01-01T00:00:11Z'
    opts       = {'logging': True, 'usecache': False}

    data, meta = hapi(server, dataset, parameter, start, stop, **opts)

    popts      = {'logging': True, 'returnimage': False, 'usecache': False}
    hapiplot(data, meta, **popts)

if False:
    server     = 'http://datashop.elasticbeanstalk.com/hapi';
    dataset    = 'CHEMS_PHA_BOX_FLUXES_FULL_TIME_RES';
    parameters = 'HPlus_BEST_T1';
    start      = '2004-07-01T04:00:00Z';
    stop       = '2004-07-01T06:00:00Z';
    opts       = {'usecache': True, 'logging': True}

    data, meta = hapi(server, dataset, parameters, start, stop, **opts)
    
    popts = {'logging': False, 'logy': True, 'logz': True}
    hapiplot(data, meta, **popts)

if False:
    server     = 'http://datashop.elasticbeanstalk.com/hapi'
    dataset    = 'CASSINI_LEMMS_PHA_PITCH_ANGLES_10_MIN'
    parameters = 'LEMMS_PHA_A_Proton'
    start      = '2004-183T00:00:00.000Z'
    stop       = '2004-183T02:00:00.000Z'
    
    opts       = {'format': 'binary', 'logging': True, 'usecache': True}
    
    data, meta = hapi(server, dataset, parameters, start, stop, **opts)
    hapiplot(data, meta)
    
    # http://localhost:8999/#server=DAS+2&dataset=Cassini/MAG/Magnitude&parameters=B_mag&start=2016-12-11T13:00:00&stop=2016-12-11T23:00&return=image&format=svg
    
    # http://hapi-server.org/servers-dev/#server=FadenTemp&dataset=Iowa+City+Conditions&parameters=Temperature&start=2022-02-11T00:00:00.000Z&stop=2022-02-12T00:00:00.000Z&return=image&format=svg
    
    