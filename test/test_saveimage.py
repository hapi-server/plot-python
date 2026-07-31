from hapiclient import hapi
from hapiplot import hapiplot

logging = False

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

  assert img1 == img2, 'Images do not match'
