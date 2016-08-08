import brewer2mpl as b2m
import matplotlib


hatchs = ['--', 'x', '+', '\\\\', '.']
markers = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd']
colors = b2m.get_map('dark2', 'qualitative', 8).mpl_colors


def to_scf(y, position):
    s = ""
    cnt = 0
    if y==0:
        return "0"
    while y>=10:
        y /= 10
        cnt += 1
    s = str(y)
    if matplotlib.rcParams['text.usetex'] is True:
        return s + r'x$10^' + str(cnt) + "$"
    else:
        return s + 'x10^' + str(cnt)


def label_all(ax, rects, rot, percent, space, lim):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        cord = height
        if cord > lim:
            cord = lim
        if percent:
            ax.text(rect.get_x() + rect.get_width()/2., cord + space,
                    '%.2f\\%%' % float(height*100),
                    rotation=rot,
                    size=7,
                    ha='center', va='top')
        else:
            ax.text(rect.get_x() + rect.get_width()/2., cord + space,
                    '%.2f' % float(height),
                    rotation=rot,
                    size=7,
                    ha='center', va='top')



def autolabel(ax, rects):
    # attach some text labels
    ylim = ax.get_ylim()
    for rect in rects:
        height = rect.get_height()
        if height >= ylim:
            ax.text(rect.get_x() + rect.get_width()/2., 1.02*ylim,
                    '%.2f' % float(height),
                    rotation=30,
                    size=5,
                    ha='center', va='top')


def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(int(100 * y))
    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] is True:
        return s + r'$\%$'
    else:
        return s + '%'


def get_hatch(i):
    return hatchs[i%len(hatchs)]


def get_marker(i):
    return markers[i%len(markers)]


def get_color(i):
    return colors[i%len(colors)]
