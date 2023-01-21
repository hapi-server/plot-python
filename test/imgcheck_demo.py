import os


if True:
    outdir = os.path.dirname(os.path.realpath(__file__))
else:
    # Put images in dir with name that depends on mpl version.
    from matplotlib import __version__ as matplotlib_version
    matplotlib_version = ".".join(matplotlib_version.split(".")[0:2])
    fdir = os.path.dirname(os.path.realpath(__file__))
    outdir = os.path.join(fdir, "imagecheck", "mpl-" + matplotlib_version)
    os.makedirs(outdir)

from matplotlib import rc_context
from matplotlib import rcParams

opts = {
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
                'figure.bbox': 'tight'
            }
}

if True:
    ref_file = os.path.join(outdir, "imgcheck_demo.ref.png")
    now_file = os.path.join(outdir, "imgcheck_demo.now.png")

    if os.path.exists(ref_file):
        os.remove(ref_file)
    if os.path.exists(now_file):
        os.remove(now_file)

    # Create ref image
    from matplotlib import pyplot as plt
    fig, ax = plt.subplots()
    ax.plot(0.25,0.25,"*")
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])

    with rc_context(rc=opts['rcParams']):
        fig.savefig(ref_file)
        fig.savefig(now_file)

    from imgcheck import imgcheck

    # Should be "PASS"
    imgcheck(ref_file, now_file)

    # Create a file that differs from ref_file
    from matplotlib import pyplot as plt
    fig, ax = plt.subplots()
    ax.plot(0.5,0.5,"o")
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])

    with rc_context(rc=opts['rcParams']):
        fig.savefig(now_file)

    # Should be "FAIL"
    imgcheck(ref_file, now_file)


if True:

    # Create ref image
    from matplotlib import pyplot as plt
    fig, ax = plt.subplots()
    ax.plot(0.25,0.25,"*")
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])

    if opts['_rcParams']['figure.bbox'] == 'tight':
        fig.tight_layout()

    from io import BytesIO
    ref_bytes = BytesIO()
    fig.canvas.print_figure(ref_bytes)
    ref_bytes = ref_bytes.getvalue()
    with open(ref_file,'wb') as f:
        f.write(ref_bytes)

    # Pass filename and bytes
    imgcheck(ref_file, ref_bytes)

    # Create a figure that differs from ref_file
    from matplotlib import pyplot as plt
    fig, ax = plt.subplots()
    ax.plot(0.5,0.5,"o")
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])

    now_bytes = BytesIO()
    fig.canvas.print_figure(now_bytes)
    now_bytes = now_bytes.getvalue()

    # Pass filename and bytes
    imgcheck(ref_file, now_bytes)
