# TODO: Change to unit tests.
# * Take screenshot of figure window canvas and compare with reference
# * Print image to file and compare with reference
# * Compare figure window screenshot with printed image.

from hapiplot.plot.heatmap import heatmap
from datetime import datetime, timedelta
import numpy as np

#tests = range(0,31)
#tests = range(27,29)
#tests = range(23,24)
tests = range(0,3)
#tests = [25]
tests = [4]

import matplotlib as plt
plt.rcParams.update({'figure.max_open_warning': 0})

import os
outdir = os.path.dirname(os.path.realpath(__file__))
outdir = os.path.join(outdir, 'heatmap_test')
if not os.path.exists(outdir):
    os.makedirs(outdir)

def testimg(fig, tn, tl):
    import os
    from imgcheck import imgcheck
    ref_file = os.path.join(outdir,'heatmap_test{0:d}{1:s}.ref.png'.format(tn,tl))
    now_file = os.path.join(outdir, 'heatmap_test{0:d}{1:s}.now.png'.format(tn,tl))
    fig.savefig(now_file)
    imgcheck(ref_file, now_file)

for tn in tests:

    # 1x1 ints
    if tn == 0:
        x = np.array([1]) # Columns
        y = np.array([1]) # Rows
        z = np.array([[1]])
        title = 'test #' + str(tn) + 'a z=1x1 int; col center and row center'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'a')

        x = np.array([1]) # Columns
        y = np.array([0,10]) # Rows
        z = np.array([[1]])
        title = 'test #' + str(tn) + 'b z=1x1 int; col center and row edges'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'b')

        x = np.array([0,10]) # Columns
        y = np.array([0,5]) # Rows
        z = np.array([[1]])
        title = 'test #' + str(tn) + 'c z=1x1 int; col edges and row edges'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'c')

    # 1x2 and 2x1 ints
    if tn == 1:
        x = np.array([1]) # Columns
        y = np.array([1,2]) # Rows
        z = np.array([[1],[2]])
        title = 'test #' + str(tn) + 'd z=2x1 ints; col center and row centers'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'a')

        x = np.array([1,2]) # Columns
        y = np.array([1,2]) # Rows
        z = np.array([[1],[2]])
        title = 'test #' + str(tn) + 'd z=2x1 ints; col edges and row centers'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'b')

        x = np.array([1]) # Columns
        y = np.array([1,2,3]) # Rows
        z = np.array([[1],[2]])
        title = 'test #' + str(tn) + 'f z=2x1 ints; col center and row edges'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'c')

        x = np.array([1,4]) # Columns
        y = np.array([1,2,3]) # Rows
        z = np.array([[1],[2]])
        title = 'test #' + str(tn) + 'g z=2x1 ints; col edges and row edges'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'d')

        x = np.array([1,2]) # Columns
        y = np.array([1]) # Rows
        z = np.array([[1,2]])
        title = 'test #' + str(tn) + 'h z=1x2 ints; col centers and row center'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'e')

        x = np.array([1,2]) # Columns
        y = np.array([1,2]) # Rows
        z = np.array([[1,2]])
        title = 'test #' + str(tn) + 'i z=1x2 ints; col centers and row edges'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'f')

        x = np.array([1,2,3]) # Columns
        y = np.array([1]) # Rows
        z = np.array([[1,2]])
        title = 'test #' + str(tn) + 'j z=1x2 ints; col edges and row center'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'g')

        x = np.array([1,3,4]) # Columns
        y = np.array([1,2.5]) # Rows
        z = np.array([[1,2]])
        title = 'test #' + str(tn) + 'k z=1x2 ints; col edges and row edges'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'h')

    # 2x2, 3x3, 10x10 ints
    if tn == 2:
        # TODO: Category for 3 should not be there (or should be white to indicate no 3s)
        x = np.array([1,2]) # Columns
        y = np.array([1,5]) # Rows
        z = np.array([[1.0,2.0],[4.0,5.0]])
        title = 'test #' + str(tn) + 'a z=2x2 ints; col centers and row centers'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'a')

        x = np.array([1,2,3]) # Columns
        y = np.array([1,2,3]) # Rows
        z = np.array([[1,2,3],[4,5,6],[7,8,9]])
        title = 'test #' + str(tn) + 'b z=3x3 ints; col centers and row centers'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'b')

        x = np.array(np.arange(1,11,1)) # Columns
        y = np.array(np.arange(1,11,1)) # Rows
        z = np.reshape(np.arange(1,101,1),(10,10))
        title = 'test #' + str(tn) + 'c z=10x10 ints; col centers and row centers'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'c')

        x = np.array(np.arange(1,11,1)) # Columns
        y = np.array(np.arange(1,11,1)) # Rows
        z = np.reshape(np.arange(1,101,1),(10,10))
        title = 'test #' + str(tn) + 'd z=10x10 ints; col centers and row centers'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'d')

    # 10x10 floats
    if tn == 3:
        # TODO: max and min on cb are not labeled.
        x = np.array(1.5+np.arange(1,11,1)) # Columns
        y = np.array(np.arange(1,11,1)) # Rows
        z = np.reshape(0.5+np.arange(1,101,1),(10,10))
        title = 'test #' + str(tn) + '  z=10x10 floats; col centers and row centers'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn)

    # Centers with non-uniform spacing
    if tn == 4:
        # Will generate warning b/c non-uniform centers
        x = np.array([1,2,3]) # Columns
        y = np.array([1,2.5,3]) # Rows
        z = np.array([[1,2,3],[4,5,6],[7,8,9]])
        title = 'test #' + str(tn) + 'a 3x3; uniform col centers nonuniform row centers + warning'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'a')

        # Will generate warning b/c non-uniform centers
        x = np.array([1,2.5,3]) # Columns
        y = np.array([1,2,3]) # Rows
        z = np.array([[1,2,3],[4,5,6],[7,8,9]])
        title = 'test #' + str(tn) + 'b 3x3; nonuniform col centers uniform row centers + warning'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'b')

        # Will generate warning b/c non-uniform centers
        x = np.array([1,2.5,3]) # Columns
        y = np.array([1,2.5,3]) # Rows
        z = np.array([[1,2,3],[4,5,6],[7,8,9]])
        title = 'test #' + str(tn) + 'c 3x3; nonuniform col centers nonuniform row centers + warning'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'c')

    # Gaps
    if tn == 5:
        x = np.array([1,2]) # Columns
        y = np.array([[1,2],[2.5,3]]) # Rows
        z = np.array([[1.0,2.0],[4.0,5.0]])
        title = 'test #' + str(tn) + 'a 2x2 col centers and row edges w/gap'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'a')

        x = np.array([[1,2],[3,4]]) # Columns
        y = np.array([[1,2],[2.5,3]]) # Rows
        title = 'test #' + str(tn) + 'b 2x2 col edges w/gap and row edges w/gap'
        z = np.array([[1.0,2.0],[4.0,5.0]])
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'b')

        x = np.array([1,2,3]) # Columns
        y = np.array([[1,2.5],[3,4],[7,8]]) # Rows
        z = np.array([[1,2,3],[4,5,6],[7,8,9]])
        title = 'test #' + str(tn) + 'c 3x3 col centers and row edges w/gaps'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'c')

        x = np.array([[1,2.5],[3,4],[7,8]]) # Columns
        y = np.array([[1,2.5],[3,4],[7,8]]) # Rows
        z = np.array([[1,2,3],[4,5,6],[7,8,9]])
        title = 'test #' + str(tn) + 'd 3x3 col edges w/gaps and row edges w/gaps'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'d')

    # NaNs
    if tn == 6:
        start = datetime(1970, 1, 1)
        tb0 = [start,start+timedelta(seconds=2.5)]
        tb1 = [start+timedelta(seconds=3),start+timedelta(seconds=4)]
        tb2 = [start+timedelta(seconds=7),start+timedelta(seconds=8)]

        y = np.array([1,2,3]) # Rows
        z = np.nan*np.array([[1,2,3],[4,5,6],[7,8,9]])

        x = np.array([1,2,3]) # Columns
        title = 'test #' + str(tn) + 'a All NaN z, uniform bins'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn+'a')

        x = [tb0, tb1, tb2]
        title = 'test #' + str(tn) + 'b All NaNs z, non-uniform x'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn+'b')

        y = np.array([[1,2.5],[3,4],[7,8]]) # Rows
        title = 'test #' + str(tn) + 'c All NaN z, non-uniform x and y'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn+'c')

    # Gaps and NaNs
    if tn == 7:
        # TODO: Need to distinguish between gaps and nans
        # With %matplotlib inline, sometimes this is cropped. Seems
        # like a bug in iPython as position of axes box differs fromt the
        # next plot below.
        x = np.array([[1,2.5],[3,4],[7,8]]) # Columns
        y = np.array([[1,2.5],[3,4],[7,8]]) # Rows
        z = np.array([[1,2,3],[4,np.nan,6],[7,8,9]])
        title = 'test #' + str(tn) + 'a 3x3 w/NaNs, col edges w/gaps. and row edges w/gaps'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'a')

        start = datetime(1970, 1, 1)
        tb0 = [start,start+timedelta(seconds=2.5)]
        tb1 = [start+timedelta(seconds=3),start+timedelta(seconds=4)]
        tb2 = [start+timedelta(seconds=7),start+timedelta(seconds=8)]

        # Gaps and NaNs
        x = np.array([tb0[1],tb1[1],tb2[1]]) # Columns
        y = np.array([[1,2.5],[3,4],[7,8]]) # Rows
        z = np.array([[1,2,3],[4,np.nan,6],[7,8,9]])
        title = 'test #' + str(tn) + 'b 3x3 w/NaNs, col edges w/gaps, and row edges w/gaps'
        opts = {
                    'title':  title,
                    'ztitle': 'ztitle',
                    'xlabel': 'xlabel',
                    'ylabel': 'ylabel',
                    'zlabel': 'zlabel'
                }
        fig, _ = heatmap(x, y, z, **opts)
        testimg(fig,tn,'b')

        start = datetime(1970, 1, 1)
        tb0 = [start,start+timedelta(seconds=2.5)]
        tb1 = [start+timedelta(seconds=3),start+timedelta(seconds=4)]
        tb2 = [start+timedelta(seconds=7),start+timedelta(seconds=8)]

        x = np.array([tb0,tb1,tb2]) # Columns
        y = np.array([[1,2.5],[3,4],[7,8]]) # Rows
        z = np.array([[1,2,3],[4,np.nan,6],[7,8,9]])
        title = 'test #' + str(tn) + 'c 3x3 w/NaNs, col edges w/gaps, and row edges w/gaps'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'c')

        start = datetime(1970, 1, 1)
        tb0 = [start,start+timedelta(seconds=2.5)]
        tb1 = [start+timedelta(seconds=3),start+timedelta(seconds=4)]
        tb2 = [start+timedelta(seconds=7),start+timedelta(seconds=8)]

        # TODO: Need to distinguish between gaps and nans
        #x = np.array([tb0,tb1,tb2]) # Columns
        x = np.array([[0,1],[2,3],[4,5]]) # Columns
        y = np.array(['A','B','C']) # Rows
        z = np.array([[1,2,3],[4,np.nan,6],[7,8,9]])
        title = 'test #' + str(tn) + 'd 3x3 ints w/NaNs, col edges, categorical y'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'d')

        start = datetime(1970, 1, 1)
        tb0 = [start,start+timedelta(seconds=2.5)]
        tb1 = [start+timedelta(seconds=3),start+timedelta(seconds=4)]
        tb2 = [start+timedelta(seconds=7),start+timedelta(seconds=8)]

        # TODO: Need to distinguish between gaps and nans
        x = np.array(['First','Second','Third']) # Columns
        y = np.array(['A','B','C']) # Rows
        z = np.array([[1,2,3],[4,np.nan,6],[7,8,9]])
        title = 'test #' + str(tn) + 'e 3x3 w/NaNs and categorical x and y'
        fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn,'e')

        start = datetime(1970, 1, 1)
        tb0 = [start,start+timedelta(seconds=2.5)]
        tb1 = [start+timedelta(seconds=3),start+timedelta(seconds=4)]
        tb2 = [start+timedelta(seconds=7),start+timedelta(seconds=8)]

        # TODO: Need to distinguish between gaps and nans
        x = np.array([tb0,tb1,tb2]) # Columns
        y = np.array([[1,2.5],[3,4],[7,8]]) # Rows
        z = np.array([[1,2,3],[4,np.nan,6],[7,8,9]])
        title = 'test #' + str(tn) + '  3x3 w/NaNs, col edges w/gaps. and row edges w/gaps'
        opts = {'title': title, 
                'nan.color': [0,1,1],
                'nan.hatch': '.',
                'nan.hatch.color':'k',
                'gap.color': [1,0,1],
                'gap.hatch': 'x',
                'gap.hatch.color':'k'}
        fig, _ = heatmap(x, y, z, **opts)
        testimg(fig,tn,'f')

    # Using rc_context
    if tn == 9:

        from matplotlib import rc_context

        rcParams = {
                    'savefig.dpi': 144,
                    'savefig.format': 'png',
                    'savefig.bbox': 'standard',
                    'savefig.transparent': True,
                    'figure.max_open_warning': 50,
                    'figure.figsize': (7, 3),
                    'figure.dpi': 144,
                    'axes.titlesize': 10}
        
        x = np.array(np.arange(1,11,1)) # Columns
        y = np.array(np.arange(1,11,1)) # Rows
        z = np.reshape(np.arange(1,101,1),(10,10))
        title = 'test #' + str(tn) + 'a using rc_context'
        with rc_context(rc=rcParams):
            fig, _ = heatmap(x, y, z, title=title, zlabel="A\nB\nC")
            testimg(fig,tn,'a')

    # TODOs
    if tn == 10:

        x = np.array(np.arange(20)) # Columns
        y = np.array(np.arange(20)) # Rows
        z = np.random.rand(20,20)

        title = 'test #' + str(tn) + 'a TODO: bottom and top limits not shown'
        fig, cb = fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn+'a')

        x = np.array([1,2,3,4]) # Columns
        y = np.array([1,2,3,4]) # Rows
        z = np.array([[0,3,0,3],[0,3,0,3],[0,3,0,3],[0,3,0,3]])
        title = 'test #' + str(tn) + 'b TODO: some colors not present'
        fig, cb = fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn+'b')

        x = np.array([1,2,3,4]) # Columns
        y = np.array([1,2,3,4]) # Rows
        z = np.array([[0,1e9,0,10],[0,10,0,10],[0,10,0,10],[0,10,0,10]])
        title = 'test #' + str(tn) + 'c TODO: large z values'
        fig, cb = fig, _ = heatmap(x, y, z, title=title)
        testimg(fig,tn+'c')
