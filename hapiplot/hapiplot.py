import os
import hashlib
import json

import numpy as np
from matplotlib import rc_context
from matplotlib import rcParams

from hapiclient.hapitime import hapitime2datetime
from hapiclient.hapi import request2path
from hapiclient.hapi import cachedir
from hapiclient.util import log, warning
from hapiplot.plot.timeseries import timeseries
from hapiplot.plot.heatmap import heatmap
from hapiplot.plot.util import setopts

def hapiplot(*args, **kwargs):
    """Plot response from HAPI server.

    Version: 0.2.3b0

    Demos
    -----
    <https://github.com/hapi-server/client-python/blob/master/hapiclient/plot/hapiplot_test.py>


    Usage
    -----
            data, meta = hapiplot(server, dataset, params, start, stop, **kwargs)
        or    
            meta = hapiplot(data, meta, **kwargs)
        where data and meta are return values from `hapi()`.

        All parameters are plotted. If a parameter has a bins attribute,
        it is plotted using `heatmap()`. Otherwise, it is plotted using
        `timeseries()`.

    Returns
    -------
        `data` is the same as that returned from `hapi()`.
        `meta` is the same as that returned from `hapi()` with the additon of

        meta['parameters'][i]['hapiplot']['figure'] is a reference to the
            figure (e.g., plt.gcf()). Usage example:

            >>> fig = meta['parameters'][i]['hapiplot']['figure']
            >>> fig.set_facecolor('blue')
            >>> fig.axes[0].set_ylabel('new y-label')
            >>> fig.axes[0].set_title('new title\\nsubtitle\\nsubtitle')
            >>> fig.tight_layout()

        meta['parameters'][i]['hapiplot']['colorbar'] is a reference to the
            colorbar on the figure (if parameter plotted as a heatmap)

        meta['parameters'][i]['hapiplot']['image'] is PNG, PDF, or SVG data
            and is included only if `returnimage=True`. Usage example:

            >>> img = meta['parameters'][i]['hapiplot']['image']
            >>> Image.open(io.BytesIO(img)).show()
            >>> # or
            >>> f = open('/tmp/a.png', 'wb')
            >>> f.write(img)
            >>> f.close()

    See Also
    ---------
        `hapi()`: Get data from a HAPI server
        `timeseries()`: Used by `hapiplot()` to HAPI parameters with no `bins`
        `heatmap()`: Used by `hapiplot()` to HAPI parameters with `bins`

        <https://github.com/hapi-server/client-python-notebooks>

    kwargs
    ------
        * logging: [False] Display console messages
        * usecache: [True] Use cached data
        * tsopts: {} kwargs for the `timeseries()` function
        * hmopts: {} kwargs for the `heatmap()` function

    Other kwargs
    ------------
        * returnimage: [False] If True, `hapiplot()` returns binary image data
        * returnformat: [png], svg, or pdf
        * cachedir: Directory to store images. Default is hapiclient.hapi.cachedir()
        * useimagecache: [True] Used cached image (when returnimage=True)
        * saveimage: [False] Save image to `cachedir`
        * saveformat: [png], svg, or pdf

    Example
    --------
        >>> server  = 'http://hapi-server.org/servers/TestData2.0/hapi'
        >>> dataset = 'dataset1'
        >>> start   = '1970-01-01T00:00:00'
        >>> stop    = '1970-01-02T00:00:00'
        >>> params  = 'scalar,vector'
        >>> opts    = {'logging': True}
        >>>
        >>> from hapiclient import hapiplot
        >>> hapiplot(server, dataset, params, start, stop, **opts)
        >>>
        >>> # or
        >>>
        >>> from hapiclient import hapi, hapiplot
        >>> data, meta = hapi(server, dataset, params, start, stop, **opts)
        >>> hapiplot(data, meta, **opts)

    """

    if len(args) == 5:
        # For consistency with gallery and autoplot functions, allow usage of
        # hapiplot(server, dataset, parameters, start, stop, **kwargs)
        from hapiclient.hapi import hapiopts
        from hapiclient.hapi import hapi
        kwargs_allowed = hapiopts()
        kwargs_reduced = {}
        # Extract hapi() options from kwargs
        for key, value in kwargs.items():
            if key in kwargs_allowed:
                kwargs_reduced[key] = value
        data, meta = hapi(args[0], args[1], args[2], args[3], args[4], **kwargs_reduced)
        meta = hapiplot(data, meta, **kwargs)
        return data, meta
    else:
        data = args[0]
        meta = args[1]

    # Default options
    opts = {
                'logging': False,
                'saveimage': False,
                'returnimage': False,
                'usecache': True,
                'useimagecache': True,
                'cachedir': cachedir(),
                'backend': 'default',
                'style': 'fast',

                'title': '',
                'ztitle': '',
                'xlabel': '',
                'ylabel': '',
                'zlabel': '',
                'logx': False,
                'logy': False,
                'logz': False,

                'tsopts': {},
                'hmopts': {},

                'rcParams':
                    {
                        'savefig.dpi': 144,
                        'savefig.format': 'png',
                        'savefig.bbox': 'tight',
                        'savefig.transparent': False,
                        'figure.max_open_warning': 50,
                        'figure.figsize': (7, 3),
                        'figure.dpi': 144,
                        'axes.titlesize': 10,
                        "font.family": "serif",
                        "font.serif": rcParams['font.serif'],
                        "font.weight": "normal"
                    },
                '_rcParams': {
                        'figure.bbox': 'standard'
                }
            }

    # Override defaults
    opts = setopts(opts, kwargs)

    from hapiclient import __version__
    log('Using hapi.py version %s' % __version__, opts)

    from hapiplot import __version__
    from matplotlib import __version__ as mpl_version

    log('hapiplot version %s using Matplotlib version %s' % \
        (__version__, mpl_version), opts)

    # _rcParams are not actually rcParams:
    # 'figure.bbox': 'standard',
    # Set to 'tight' to have fig.tight_layout() called before figure shown.

    if opts["saveimage"]:
        # Create cache directory
        dir = cachedir(opts['cachedir'], meta['x_server'])
        if not os.path.exists(dir): os.makedirs(dir)

    # Convert from NumPy array of byte literals to NumPy array of
    # datetime objects.
    timename = meta['parameters'][0]['name']

    nodata = False
    if len(data[timename]) == 0:
        nodata = True
        # Set time to request range to set x-axis
        Time = hapitime2datetime(np.array([meta['x_time.min'], meta['x_time.max']]), allow_missing_Z=True)
    else:
        Time = hapitime2datetime(data[timename], allow_missing_Z=True)

    if len(meta["parameters"]) == 1:
        a = 0 # Time is only parameter
    else:
        a = 1 # Time plus one or more parameters

    for i in range(a, len(meta["parameters"])):

        meta["parameters"][i]['hapiplot'] = {}

        name = meta["parameters"][i]["name"]

        if len(data[name].shape) > 3:
            # TODO: Implement more than 2 dimensions?
            log("Parameter '%s' has more than two components. Skipping." % name, opts)
            continue

        # If parameter has a size with two elements, e.g., [N1, N2]
        # create N2 plots.
        if len(data[name].shape) == 3:  # shape = (Time, N1, N2)

            log("Parameter '%s' has 3 components. Creating one plot per component." % name, opts)

            pidx = 1 # Primary (fastest varying) index is N2
            sidx = 0 # Secondary index is N1
            nplts = data[name].shape[1]
            if data[name].shape[1] > data[name].shape[2]:
                pidx = 0
                sidx = 1
                nplts = data[name].shape[2]

            if opts['returnimage']:
                warning('Only returning first image for parameter with size[1] > 1.')
                nplts = 1

            for j in range(nplts):
                timename = meta['parameters'][0]['name']

                # Name to indicate what is plotted
                if pidx > sidx:
                    name_new = name + "[" + str(j) + ",:]"
                else:
                    name_new = name + "[:," + str(j) + "]"

                # Reduced data ND Array
                datar = np.ndarray(shape=(data[name].shape[0]),
                                   dtype=[
                                           (timename, data.dtype[timename]),
                                           (name_new, data[name].dtype.str, 
                                            data[name].shape[1+pidx])
                                         ])

                datar[timename] = data[timename]
                if pidx > sidx:
                    datar[name_new] = data[name][:, j, :]
                else:
                    datar[name_new] = data[name][:, :, j]

                # Copy metadata to create a reduced metadata object
                metar = meta.copy()  # Shallow copy
                metar["parameters"] = []
                # Create parameters array with elements of Time parameter ...
                metar["parameters"].append(meta["parameters"][0])
                # .... and this parameter
                metar["parameters"].append(meta["parameters"][i].copy())
                # Give new name to indicate it is a subset of full parameter
                metar["parameters"][1]['name'] = name_new
                metar["parameters"][1]['name_orig'] = name

                # New size is N1 or N2
                metar["parameters"][1]['size'] = [meta["parameters"][i]['size'][pidx]]

                if 'units' in metar["parameters"][1]:
                    if type(meta["parameters"][i]['units']) == str or meta["parameters"][i]['units'] == None:
                        # Same units applies to all dimensions
                        metar["parameters"][1]["units"] = meta["parameters"][i]['units']
                    else:
                        metar["parameters"][1]["units"] = meta["parameters"][i]['units'][j]

                if 'label' in metar["parameters"][1]:
                    if type(meta["parameters"][i]['label']) == str:
                        # Same label applies to all dimensions
                        metar["parameters"][1]["label"] = meta["parameters"][i]['label']
                    else:
                        metar["parameters"][1]["label"] = meta["parameters"][i]['label'][j]

                # Extract bins corresponding to jth column of data[name]
                if 'bins' in metar["parameters"][1]:
                    metar["parameters"][1]['bins'] = []
                    metar["parameters"][1]['bins'].append(meta["parameters"][i]['bins'][pidx])


                bin_title = ""
                if 'bins' in meta["parameters"][i] and len(meta["parameters"][i]['bins']) > 1:
                    bin_title = meta["parameters"][i]['bins'][sidx]['name']
                    if 'centers' in meta["parameters"][i]['bins'][sidx]:
                        bin_title = bin_title  + " = " + str(meta["parameters"][i]['bins'][sidx]['centers'][j])
                        if 'units' in meta["parameters"][i]['bins'][sidx]:
                            if meta["parameters"][i]['bins'][sidx]['units'] is not None:
                                bin_title = bin_title + " [" + meta["parameters"][i]['bins'][sidx]['units'] + "]"
                            bin_title = "\n" + bin_title

                opts['title'] = meta["x_server"] + "\n" + meta["x_dataset"] + " | " + name_new + bin_title

                # rcParams is modified by setopts to have all rcParams.
                # reset to original passed rcParams so that imagepath
                # computes file name based on rcParams passed to hapiplot.
                if 'rcParams' in kwargs:
                    opts['rcParams'] = kwargs['rcParams']

                metar = hapiplot(datar, metar, **opts)

                meta["parameters"][i]['hapiplot'] = metar["parameters"][1]['hapiplot']
            return meta

        # Return cached image (case where we are returning binary image data)
        # imagepath() options. Only need filename under these conditions.
        if opts['saveimage'] or (opts['returnimage'] and opts['useimagecache']):
            # Will use given rc style parameters and style name to generate file name.
            # Assumes rc parameters of style and hapiplot defaults never change.
            styleParams = {}
            fmt = opts['rcParams']['savefig.format']
            if 'rcParams' in kwargs:
                styleParams = kwargs['rcParams']
                if 'savefig.format' in kwargs['rcParams']:
                    kwargs['rcParams']['savefig.format']

            fnameimg = imagepath(meta, i, opts['cachedir'], styleParams, fmt)

        if opts['useimagecache'] and opts['returnimage'] and os.path.isfile(fnameimg):
            log('Returning cached binary image data in ' + fnameimg, opts)

            meta["parameters"][i]['hapiplot']['imagefile'] = fnameimg
            with open(fnameimg, "rb") as f:
                meta["parameters"][i]['hapiplot']['image'] = f.read()
            continue

        log("Plotting parameter '%s'" % name, opts)

        if opts['title'] != '':
            title = opts['title']
        else:
            if 'name_orig' in meta["parameters"][i]:
                title = meta["x_server"] + "\n" + meta["x_dataset"] + " | " + meta["parameters"][i]['name_orig']
            else:
                title = meta["x_server"] + "\n" + meta["x_dataset"] + " | " + name

        as_heatmap = False
        if 'size' in meta['parameters'][i] and meta['parameters'][i]['size'][0] > 10:
            as_heatmap = True

        if 'bins' in meta['parameters'][i]:
            as_heatmap = True

        if 'units' in meta["parameters"][i] and type(meta["parameters"][i]["units"]) == list:
            if as_heatmap:
                # TODO: Verify that all units not the same
                warning("Not plotting %s as heatmap because components have different units." % meta["parameters"][i]["name"])
            as_heatmap = False

        if as_heatmap:
            # Plot as heatmap

            hmopts = {
                        'returnimage': opts['returnimage'],
                        'transparent': opts['rcParams']['savefig.transparent']
                    }

            if meta["parameters"][i]["type"] == "string":
                warning("Plots for only types double, integer, and isotime implemented. Not plotting %s." % meta["parameters"][i]["name"])
                continue

            if nodata:
                if a == 0:
                    # Time is only parameter
                    z = np.full((2,), np.nan)
                else:
                    if 'size' in meta['parameters'][i]:
                        z = np.full((2, meta['parameters'][i]['size'][0]), np.nan)
                    else:
                        z = np.full((2,), np.nan)
            else:
                z = np.asarray(data[name])

            if 'fill' in meta["parameters"][i] and meta["parameters"][i]['fill']:
                if meta["parameters"][i]["type"] == 'integer':
                    z = z.astype('<f8', copy=False)
                z = fill2nan(z, meta["parameters"][i]['fill'])

            units = meta["parameters"][i]["units"]
            nl = ""
            if len(name) + len(units) > 30:
                nl = "\n"

            #zlabel = name + nl + " [" + units + "]"
            zlabel = "";
            if units is not None:
                zlabel = " [" + units + "]"

            bins = np.arange(meta['parameters'][i]['size'][0])
            bins_time_dependent = False
            if 'bins' in meta['parameters'][i]:
                if 'ranges' in meta["parameters"][i]['bins'][0]:
                    if isinstance(meta['parameters'][i]['bins'][0]['ranges'], str) is False:
                        bins = np.array(meta["parameters"][i]['bins'][0]["ranges"])
                    else:
                        bins_time_dependent = True
                else:
                    if isinstance(meta['parameters'][i]['bins'][0]['centers'], str) is False:
                        bins = np.array(meta["parameters"][i]['bins'][0]["centers"])
                    else:
                        bins_time_dependent = True

            if 'bins' in meta['parameters'][i] and not bins_time_dependent:
                ylabel = meta["parameters"][i]['bins'][0]["name"] \
                       + " [" \
                       + meta["parameters"][i]['bins'][0]["units"] \
                       + "]"
            else:
                ylabel = "bin #"
                if bins_time_dependent:
                    ylabel = "bin #\n(vals are time dependent)"

            dt = np.diff(Time)
            dtu = np.unique(dt)
            if len(dtu) > 1:
                warning('Time values are not uniformly spaced. Bin width for '
                        'time will be based on time separation of consecutive time values.')
                # Cadence != time bin width in general, so can't use cadence.
                # See https://github.com/hapi-server/data-specification/issues/75
                if 'timeStampLocation' in meta and meta['timeStampLocation'].lower() == "begin":
                    deltat = dt[0]
                    for t in range(0,Time.size):
                        Time[t] = Time[t] + dt[t]
                elif 'timeStampLocation' in meta and meta['timeStampLocation'].lower() == "end":
                    for t in range(0,Time.size):
                        deltat = -dt[0]
                        Time[t] = Time[t] - dt[i]
                else:
                    deltat = -dt[0]/2

                for t in range(0,Time.size):
                    Time[t] = Time[t] + deltat
 
                Time = np.append(Time, Time[-1] + dt[-1])

            elif 'timeStampLocation' in meta:
                if meta['timeStampLocation'].lower() == "begin":
                    Time = np.append(Time, Time[-1] + dtu[0])
                elif meta['timeStampLocation'].lower() == "end":
                    Time = Time - dtu[0]
                    Time = np.append(Time, Time[-1] + dtu[0])
                else:
                    Time = Time - dtu[0]/2
                    Time = np.append(Time, Time[-1] + dtu[0])

            if opts['xlabel'] != '' and 'xlabel' not in opts['hmopts']:
                hmopts['xlabel'] = opts['xlabel']

            opts['hmopts']['ylabel'] = ylabel
            if opts['ylabel'] != '' and 'ylabel' not in opts['hmopts']:
                hmopts['ylabel'] = opts['ylabel']

            opts['hmopts']['title'] = title
            if opts['title'] != '' and 'title' not in opts['hmopts']:
                hmopts['title'] = opts['title']

            opts['hmopts']['zlabel'] = zlabel
            if opts['zlabel'] != '' and 'zlabel' not in opts['hmopts']:
                hmopts['zlabel'] = opts['zlabel']

            if False:
                opts['hmopts']['ztitle'] = ztitle
                if opts['ztitle'] != '' and 'ztitle' not in opts['hmopts']:
                    hmopts['ztitle'] = opts['ztitle']

            if opts['logx'] is not False:
                hmopts['logx'] = True
            if opts['logy'] is not False:
                hmopts['logy'] = True
            if opts['logz'] is not False:
                hmopts['logz'] = True

            for key, value in opts['hmopts'].items():
                hmopts[key] = value

            with rc_context(rc=opts['rcParams']):
                fig, cb = heatmap(Time, bins, np.transpose(z), **hmopts)

            meta["parameters"][i]['hapiplot']['figure'] = fig
            meta["parameters"][i]['hapiplot']['colorbar'] = cb

        else:

            tsopts = {
                        'logging': opts['logging'],
                        'returnimage': opts['returnimage'],
                        'transparent': opts['rcParams']['savefig.transparent'],
                        'backend': opts['backend']
                    }

            ptype = meta["parameters"][i]["type"]
            if nodata:
                if a == 0:
                    # Time is only parameter
                    y = np.full((2,), np.nan)
                else:
                    if 'size' in meta['parameters'][i]:
                        y = np.full((2,meta['parameters'][i]['size'][0]), np.nan)
                    else:
                        y = np.full((2,), np.nan)
            else:
              if ptype == "isotime":
                  y = hapitime2datetime(data[name],allow_missing_Z=True)
              elif ptype == 'string':
                  y = data[name].astype('U')
              else:
                  y = np.asarray(data[name])

            if 'fill' in meta["parameters"][i] and meta["parameters"][i]['fill']:
                if nodata == False and ptype == 'isotime' or ptype == 'string':
                    Igood = y != meta["parameters"][i]['fill']
                    # Note that json reader returns fill to U not b.
                    Nremoved = data[name].size - Igood.size
                    if Nremoved > 0:
                        # TODO: Implement masking so connected line plots will
                        # show gaps as they do for NaN values.
                        warning('Parameter ' + name + ' is of type ' + ptype + ' and has '
                                + str(Nremoved) + ' fill value(s). Masking is not implemented, '
                                'so removing fill elements before plotting.')
                        Time = Time[Igood]
                        y = y[Igood]
                if ptype == 'integer':
                    y = y.astype('<f8', copy=False)
                if ptype == 'integer' or ptype == 'double':
                    y = fill2nan(y, meta["parameters"][i]['fill'])

            remove_mean = False
            if 'uk/GIN_' in meta['x_server'] and (ptype == 'integer' or ptype == 'double'):
                remove_mean = True
                y_mean = np.nanmean(y, axis=0)

            units = None
            if 'units' in meta["parameters"][i] and meta["parameters"][i]['units']:
                units = meta["parameters"][i]["units"]


            nl = ""
            if type(units) == str:
                if len(name) + len(units) > 30:
                    nl = "\n" # TODO: Automatically figure out when this is needed.

            ylabel = name
            if units is not None and type(units) is not list:
                ylabel = name + nl + " [" + units + "]"

            if type(units) == list:
                ylabel = name

            if not 'legendlabels' in opts['tsopts']:
                legendlabels = []
                if 'size' in meta['parameters'][i]:
                    for l in range(0,meta['parameters'][i]['size'][0]):
                        bin_label = ''
                        bin_name = ''
                        col_name = ''
                        if 'bins' in meta['parameters'][i]:
                            bin_name = meta['parameters'][i]['bins'][0]['name']
                            if 'label' in meta['parameters'][i]['bins'][0]:
                                if type(meta['parameters'][i]['bins'][0]['label']) == str:
                                    bin_name = meta['parameters'][i]['bins'][0]['label']
                                else:
                                    bin_name = meta['parameters'][i]['bins'][0]['label'][l]
                            sep = ''
                            if 'centers' in meta['parameters'][i]['bins'][0] and 'ranges' in meta['parameters'][i]['bins'][0]:
                                bin_name = bin_name + ' bin with'
                                sep = ';'

                            bin_label = ''

                            if 'units' in meta['parameters'][i]['bins'][0]:
                                bin_units = meta['parameters'][i]['bins'][0]['units']
                                if type(bin_units) == list:
                                    if type(bin_units[l]) == str and bin_units != '':
                                        bin_units = ' [' + bin_units[l] + ']'
                                    elif bin_units[l] == None:
                                        bin_units = ' '
                                    else:
                                        bin_units = ' '
                                else:
                                    if type(bin_units) == str and bin_units != '':
                                       bin_units = ' [' + bin_units + ']'
                                    else:
                                       bin_units = ' '

                            if 'centers' in meta['parameters'][i]['bins'][0]:
                                if meta['parameters'][i]['bins'][0]['centers'][l] is not None:
                                    bin_label = bin_label + ' center = ' + str(meta['parameters'][i]['bins'][0]['centers'][l]) + bin_units
                                #else:
                                #   bin_label = bin_label + ' center = None'

                            if 'ranges' in meta['parameters'][i]['bins'][0]:
                                if type(meta['parameters'][i]['bins'][0]['ranges'][l]) == list:
                                    if meta['parameters'][i]['bins'][0]['ranges'][l][0] and meta['parameters'][i]['bins'][0]['ranges'][l][1] is not None:
                                        bin_label = bin_label + sep + ' range = [' + str(meta['parameters'][i]['bins'][0]['ranges'][l][0]) + ', ' + str(meta['parameters'][i]['bins'][0]['ranges'][l][1]) + ']' + bin_units
                                #else:
                                #    bin_label = bin_label + sep + ' range = [None]'

                            if bin_label != '':
                                bin_label = 'bin: ' + bin_label
                                col_name = bin_name + '#%d' % l

                        if col_name == '':
                            col_name = 'col #%d' % l

                        if nodata:
                            col_name = col_name + " [no data in interval]"

                        if remove_mean:
                            if y_mean[l] > 0:
                                col_name = "{0:s} - {1:.2f}".format(col_name, y_mean[l])
                            if y_mean[l] < 0:
                                col_name = "{0:s} + {1:.2f}".format(col_name, -y_mean[l])

                        if 'label' in meta['parameters'][i] and \
                            type(meta['parameters'][i]['label']) == list and \
                            len(meta['parameters'][i]['label']) > l and \
                            meta['parameters'][i]['label'][l].strip() != '':
                                col_name = meta['parameters'][i]['label'][l]
                                if nodata:
                                    col_name = col_name + " [no data in interval]"
                                else:
                                    if remove_mean:
                                        if y_mean[l] > 0:
                                            col_name = "{0:s} - {1:.2f}".format(col_name, y_mean[l])
                                        if y_mean[l] < 0:
                                            col_name = "{0:s} + {1:.2f}".format(col_name, -y_mean[l])


                        if type(units) == list:
                            if len(units) == 1:
                                if units[0] != '':
                                    legendlabels.append(col_name + ' [' + units[0] + '] ' + bin_label)
                            elif type(units[l]) == str and units[l] != '':
                                legendlabels.append(col_name + ' [' + units[l] + '] ' + bin_label)
                            elif units[l] == None:
                                legendlabels.append(col_name + ' ' + bin_label)
                            else:
                                legendlabels.append(col_name + ' ' + bin_label)
                        else:
                            # Units are on y label
                            legendlabels.append(col_name + ' ' + bin_label)
                    tsopts['legendlabels'] = legendlabels

            # If xlabel in opts and opts['tsopts'], warn?
            if opts['xlabel'] != '' and 'xlabel' not in opts['tsopts']:
                tsopts['xlabel'] = opts['xlabel']

            tsopts['ylabel'] = ylabel
            if opts['ylabel'] != '' and 'ylabel' not in opts['tsopts']:
                tsopts['ylabel'] = opts['ylabel']

            tsopts['title'] = title
            if opts['title'] != '' and 'title' not in opts['tsopts']:
                tsopts['title'] = opts['title']

            if opts['logx'] is not False and 'logx' not in opts['tsopts'] :
                tsopts['logx'] = True
            if opts['logy'] is not False and 'logy' not in opts['tsopts']:
                tsopts['logy'] = True

            # Apply tsopts
            for key, value in opts['tsopts'].items():
                tsopts[key] = value

            if nodata == True:
                tsopts['nodata'] = True

            if remove_mean:
                with rc_context(rc=opts['rcParams']):
                    fig = timeseries(Time, y-y_mean, **tsopts)
            else:
                with rc_context(rc=opts['rcParams']):
                    fig = timeseries(Time, y, **tsopts)
            if remove_mean:
                with rc_context(rc=opts['rcParams']):
                    fig = timeseries(Time, y-y_mean, **tsopts)
            else:
                with rc_context(rc=opts['rcParams']):
                    fig = timeseries(Time, y, **tsopts)

            meta["parameters"][i]['hapiplot']['figure'] = fig


        if opts['saveimage']:
            log('Writing %s' % fnameimg, opts)
            meta["parameters"][i]['hapiplot']['imagefile'] = fnameimg
        else:
            from io import BytesIO
            fnameimg = BytesIO()

        if opts['returnimage']:
            with rc_context(rc=opts['rcParams']):
                fig.canvas.print_figure(fnameimg)

            if opts['saveimage']:
                with open(fnameimg, mode='rb') as f:
                    meta["parameters"][i]['hapiplot']['image'] = f.read()
            else:
                meta["parameters"][i]['hapiplot']['image'] = fnameimg.getvalue()
        else:
            with rc_context(rc=opts['rcParams']):
                fig.savefig(fnameimg)

            # Two calls to fig.tight_layout() may be needed b/c of bug in PyQt:
            # https://github.com/matplotlib/matplotlib/issues/10361
            if opts['_rcParams']['figure.bbox'] == 'tight':
                fig.tight_layout()

    return meta


def imagepath(meta, i, cachedir, opts, fmt):

    # The value of axis.prop_cycle is a cycler
    # https://matplotlib.org/cycler/
    # and can't be serialized by json.dumps.
    if 'axes.prop_cycle' in opts:
        opts['axes.prop_cycle'] = list(opts['axes.prop_cycle'])

    try:
        optsmd5 = hashlib.md5(json.dumps(opts, sort_keys=True).encode('utf8')).hexdigest()
    except:
        # Remove elements that can't be serialized.
        for key in opts:
            try:
                json.dumps(opts[key])
            except:
                #print('Removed ' + key)
                opts[key] = None
        optsmd5 = hashlib.md5(json.dumps(opts, sort_keys=True).encode('utf8')).hexdigest()

    fname = request2path(meta['x_server'],
                         meta['x_dataset'],
                         meta['parameters'][i]['name'],
                         meta['x_time.min'],
                         meta['x_time.max'],
                         cachedir)

    return fname + "-" + optsmd5 + "." + fmt


def fill2mask(y, fill):
    """Create a masked array for a non-numeric fill value."""

    # TODO: Write. Needed for ISOTime parameters with a fill value.
    pass


def fill2nan(y, fill):

    if fill.lower() == 'nan':
        yfill = np.nan
    else:
        yfill = float(fill)

    # Replace fills with NaN for plotting
    # (so gaps shown in lines for time series an empty tiles for spectra)
    y[y == yfill] = np.nan
    # Catch case values in binary where, e.g., metadata says fill='-1E-31'
    # but file has -9.999999848243207e+30. This happens when CDF data
    # values stored as floats is converted to binary using double(value)
    # because double(float('-1E31')) = -9.999999848243207e+30. Technically
    # the server is not producing valid results b/c spec says fill values
    # in file must match double(fill string in metadata).
    y[y == np.float32(yfill)] = np.nan

    return y
