from hapiclient import hapi
from hapiplot import hapiplot

# http://localhost:8999/#server=DAS+2&dataset=Cassini/MAG/Magnitude&parameters=B_mag&start=2016-12-11T13:00:00&stop=2016-12-11T23:00&return=image&format=svg
# http://hapi-server.org/servers-dev/#server=FadenTemp&dataset=Iowa+City+Conditions&parameters=Temperature&start=2022-02-11T00:00:00.000Z&stop=2022-02-12T00:00:00.000Z&return=image&format=svg

all = False
bn = 14

if bn == 1 or all == True:
    server     = 'http://hapi-server.org/servers-dev/TestData2.1/hapi'
    dataset    = 'dataset1'
    parameter  = 'matrix'
    start      = '1970-01-01Z'
    stop       = '1970-01-01T00:00:11Z'
    opts       = {'logging': True, 'usecache': True}

    data, meta = hapi(server, dataset, parameter, start, stop, **opts)

    popts      = {'logging': True, 'returnimage': True, 'usecache': False}
    hapiplot(data, meta, **popts)

if bn == 2 or all == True:
    # CDAWeb data - Magnitude and BGSEc from dataset AC_H0_MFI
    server     = 'https://cdaweb.gsfc.nasa.gov/hapi'
    dataset    = 'AC_H0_MFI'
    start      = '1997-12-10T00:00:00'
    stop       = '1997-12-11T10:00:00'
    parameters = 'Magnitude,BGSEc'
    opts       = {'logging': True, 'usecache': True}    
    data, meta = hapi(server, dataset, parameters, start, stop, **opts)
    hapiplot(data, meta, **opts)
    
    opts['returnimage'] = True
    meta = hapiplot(data, meta, **opts)
    fig = meta['parameters'][1]['hapiplot']['figure']

if bn == 3 or all == True:
    server     = 'http://hapi-server.org/servers/SSCWeb/hapi'
    dataset    = 'rbspa'
    start      = '2012-08-31T00:00:00.000Z'
    stop       = '2012-08-31T23:59:59.999Z'
    parameters = 'Time'
    opts       = {'logging': True, 'usecache': True}    
    data, meta = hapi(server, dataset, parameters, start, stop, **opts)
    hapiplot(data, meta, **opts)

if bn == 4 or all == True:
    # Empty response not handled by hapiclient.

    server     = 'https://hapi-server.org/servers-dev/CAIO/hapi'
    dataset    = 'C1_CP_CIS-CODIF_HS_H1_MOMENTS'
    parameter  = 'duration__C1_CP_CIS-CODIF_HS_H1_MOMENTS'
    #start      = '2013-11-25T16:00:00.000Z'
    #stop       = '2013-11-25T16:59:59.999Z'
    start      = '2001-01-01T00:00:00.000Z'
    stop       = '2001-01-01T01:00:00.000Z'

    opts       = {'logging': True, 'usecache': True}

    data, meta = hapi(server, dataset, parameter, start, stop, **opts)

    popts      = {'logging': True, 'returnimage': False, 'usecache': False}
    hapiplot(data, meta, **popts)

if bn == 5 or all == True:

    # Showing image in IPython requires display(SVG(...))
    # Was not a bug, but was getting errors when trying to view
    # output when returnimage=True

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

    from IPython.display import display, SVG
    display(SVG(meta['parameters'][1]['hapiplot']['image']))

if bn == 6 or all == True:

    # Handling of no data in interval

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

if bn == 7 or all == True:
    
    # Resulted in error previously because times without trailing Z
    # were considered error by hapitime2datetime(). Now hapiplot() allows
    # this py passing allow_missing_Z=True to hapitime2datetime().
    
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

if bn == 8 or all == True:

    # Previously interpretation of size was backwards. Here size=[2,3] which
    # means two sets of 3-component vectors.
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

if bn == 9 or all == True:
    
    # Previously size was mis-interpreted (see bn = 8).

    server     = 'http://datashop.elasticbeanstalk.com/hapi';
    dataset    = 'CHEMS_PHA_BOX_FLUXES_FULL_TIME_RES';
    parameters = 'HPlus_BEST_T1';
    start      = '2004-07-01T04:00:00Z';
    stop       = '2004-07-01T06:00:00Z';
    opts       = {'usecache': True, 'logging': True}

    data, meta = hapi(server, dataset, parameters, start, stop, **opts)
    
    popts = {'logging': False, 'logy': True, 'logz': True}
    hapiplot(data, meta, **popts)

if bn == 10 or all == True:

    # Similar to bn = 8 and bn = 9.

    server     = 'http://datashop.elasticbeanstalk.com/hapi'
    dataset    = 'CASSINI_LEMMS_PHA_PITCH_ANGLES_10_MIN'
    parameters = 'LEMMS_PHA_A_Proton'
    start      = '2004-183T00:00:00.000Z'
    stop       = '2004-183T02:00:00.000Z'
    
    opts       = {'format': 'binary', 'logging': True, 'usecache': True}
    
    data, meta = hapi(server, dataset, parameters, start, stop, **opts)
    hapiplot(data, meta)

if bn == 11 or all == True:
    server     = 'https://jfaden.net/HapiServerDemo/hapi'
    dataset    = 'atticTemperature'
    parameters = 'Temperature'
    start      = '2022-03-06T00:00:00.000Z'
    stop       = '2022-03-07T00:00:00.000Z'

    opts       = {'format': 'binary', 'logging': True, 'usecache': True}

    data, meta = hapi(server, dataset, parameters, start, stop, **opts)
    hapiplot(data, meta)

if bn == 12 or all == True:
    server     = 'https://jfaden.net/HapiServerDemo/hapi'
    dataset    = 'atticTemperature'
    parameters = 'Temperature'
    start      = '2003-10-20T00:00:00Z'
    stop       = '2003-11-30T00:00:00.000Z'

    opts       = {'format': 'binary', 'logging': True, 'usecache': True}

    data, meta = hapi(server, dataset, parameters, start, stop, **opts)
    hapiplot(data, meta)

if bn == 13 or all == True:
    server     = 'http://planet.physics.uiowa.edu/das/das2Server/hapi'
    dataset    = 'Cassini/RPWS/Survey_KeyParam,B'
    parameters = 'magnetic_specdens'
    start      = '2010-01-01T00:00:00'
    stop       = '2010-01-02T00:00:00'

    opts       = {'format': 'binary', 'logging': True, 'usecache': True}

    data, meta = hapi(server, dataset, parameters, start, stop, **opts)
    hapiplot(data, meta)

if bn == 14 or all == True:

    from hapiclient import hapi
    
    server     = 'https://cdaweb.gsfc.nasa.gov/hapi'
    dataset    = 'GOES13_EPS-MAGED_1MIN'
    # Notes:
    # 1. Use parameters='' to request all parameters from GOES13_EPS-MAGED_1MIN.
    # 2. Multiple parameters can be requested using a comma-separated
    #    list, e.g., parameters='dtc_cor_eflux_stack9,dtc_cor_eflux_stack6'
    parameters = 'dtc_cor_eflux_stack9'
    start      = '2010-06-02T00:00:00Z'
    stop       = '2010-06-03T00:00:00.000Z'
    
    data, meta = hapi(server, dataset, parameters, start, stop)
    
    from hapiplot import hapiplot
    hapiplot(data, meta)

if bn == 15 or all == True:
    server     = 'http://hapi-server.org/servers-dev/TestData2.0/hapi'
    dataset    = 'dataset1'
    parameter  = 'spectra'
    start      = '1970-01-01T00:00:00Z'
    stop       = '1970-01-01T00:00:01Z'
    opts       = {'logging': True, 'usecache': True}

    data, meta = hapi(server, dataset, parameter, start, stop, **opts)

    popts      = {'logging': True, 'returnimage': False, 'usecache': False}
    hapiplot(data, meta, **popts)

if bn == 16 or all == True:
    # Should be "no data"
    server     = 'http://hapi-server.org/servers-dev/TestData2.0/hapi'
    dataset    = 'dataset1'
    parameter  = 'scalar'
    start      = '1970-01-01T00:00:11Z'
    stop       = '1970-01-01T00:00:12Z'
    opts       = {'logging': True, 'usecache': False, 'logging': True, 'format': 'csv'}

    data, meta = hapi(server, dataset, parameter, start, stop, **opts)
    print(data)
    popts      = {'logging': True, 'returnimage': False, 'usecache': False}
    hapiplot(data, meta, **popts)
