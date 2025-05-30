from platform import platform
import matplotlib as mpl
import matplotlib.pyplot as plt


mpl.style.use('ggplot')

rcconfig = {
    'figure.titlesize': 30,
    'figure.titleweight': 'bold',
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.major.width': 3,
    'ytick.major.width': 3,
    'xtick.major.size': 9,
    'ytick.major.size': 9,
    'xtick.top': True,
    'ytick.right': True,
    'font.family': 'Times New Roman',
    'font.weight': 'bold',
    'font.size': 24,
    'mathtext.fontset': 'stix',
    'lines.linewidth': 3,
    'axes.linewidth': 3,
    'axes.formatter.use_mathtext': True,
    'axes.labelsize': 24,
    'axes.labelweight': 'bold',
    'axes.titleweight': 'bold',
}
mpl.rcParams.update(rcconfig)

