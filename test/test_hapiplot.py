import os 

from hapiclient import hapi
from hapiplot import hapiplot

from imgcheck import imgcheck

from matplotlib import __version__ as matplotlib_version
matplotlib_version = ".".join(matplotlib_version.split(".")[0:2])

logging = False

# If True, opens diff image
show_diff = False

# If True, execute diff code; otherwise plot what would be used for diff
do_diff = True 

# If True, overwrites reference images and creates new ones
generate_ref_files = False

def test_versions():
    for version in ['2.0', '2.1', '3.0']:
        _test_version(version)

def _test_version(version):

    server  = f'http://hapi-server.org/servers/TestData{version}/hapi'
    dataset = 'dataset1'
    start   = '1970-01-01Z'
    stop    = '1970-01-01T00:00:11Z'
    if version == '3.0':
        stop = '1970-01-01T00:02:00Z'

    opts = {'logging': logging, 'usecache': False}

    meta = hapi(server, dataset, **opts)

    for i in range(0,len(meta['parameters'])):
        parameter  = meta['parameters'][i]['name']
        data, metax = hapi(server, dataset, parameter, start, stop, **opts)

        popts = {'useimagecache': False, 'logging': logging, 'returnimage': do_diff}

        if version == '2.1' and parameter == 'matrix':
            # The string 
            #   '$\Delta T_{xy}=1$'
            # causes the error
            #    Unknown symbol: \Delta, found '\'  (at char 0), (line:1, col:1)
            # only when FigCanvasAgg is the back-endfor Matplotlib 3.2.2 and 3.4.2
            # The string
            #   '$\Delta$ $T_{xy}=1$'
            # does not cause an error. Seems to be a bug in Matplotlib.
            metax['parameters'][1]['label'][0][1] = r'$\Delta$ $T_{xy}=1$'

        metap = hapiplot(data, metax, **popts)

        if do_diff == False:
            continue

        idx = 1
        if i == 0: # Time parameter
            idx = 0

        img2 = metap['parameters'][idx]['hapiplot']['image']

        dir_path = os.path.dirname(os.path.realpath(__file__))
        ref_dir = os.path.join(dir_path, "imgs", f"hapi-{version}", "mpl-" + matplotlib_version)
        ref_file = os.path.join(ref_dir, parameter + ".ref.png")

        imgcheck(ref_file, img2, show_diff=show_diff, generate_ref_files=generate_ref_files)


def test_saveimage():
    # Returned image should be same when saveimage is True or False

    server     = 'http://hapi-server.org/servers/TestData2.0/hapi'
    dataset    = 'dataset1'
    start      = '1970-01-01Z'
    stop       = '1970-01-01T00:00:11Z'
    parameters = 'scalar'
    opts       = {'logging': logging, 'usecache': True}
    data, meta = hapi(server, dataset, parameters, start, stop, **opts)

    popts = {
                 'usecache': True,
                 'useimagecache': False,
                 'logging': logging,
                 'saveimage': False,
                 'returnimage': True
             }

    meta = hapiplot(data, meta, **popts)
    img1 = meta['parameters'][1]['hapiplot']['image']
    #Image.open(io.BytesIO(img1)).show()

    popts['saveimage'] = True
    meta = hapiplot(data, meta, **popts)
    img2 = meta['parameters'][1]['hapiplot']['image']
    #Image.open(io.BytesIO(img1)).show()

    if img1 != img2:
        print('Images do not match')
        return False

    return True


if __name__ == '__main__':
    _test_version('2.0')
    _test_version('2.1')
    _test_version('3.0')
    test_saveimage()