from numpy.random import rand
from pylab import figure, show

import numpy as np
class PointBrowser:
    """
    pass a subplot to __init__
    overwrite the yellow circle on the clicked data
    """
    def __init__(self, fig, ax):
        self.fig = fig
        self.text = ax.text(0.05, 0.95, 'selected: none',
                            transform=ax.transAxes, va='top')


        self.selected,  = ax.plot([], [], 'o', ms=12, alpha=0.4,
                                  color='yellow', visible=False)

    def onpick(self, event):
        """
        it picks up the index of clicked data

        """
        if not len(event.ind):
            return True

        ind = event.ind[0]
        x = event.artist.get_xdata()[ind]
        y = event.artist.get_ydata()[ind]
        clicked = (x, y)

        self.selected.set_visible(True)
        self.selected.set_data(clicked)
        self.text.set_text(' x: %f\n y: %f'%(clicked))
        self.fig.canvas.draw()

if __name__ == "__main__":
    xs = rand(100)
    ys = rand(100)

    fig = figure()
    ax = fig.add_subplot(111)
    ax.set_title('picking demo')
    ax.plot(xs, ys, 'o', picker=5)  # 5 points tolerance

    browser = PointBrowser(fig, ax)
    fig.canvas.mpl_connect('pick_event', browser.onpick)

    show()
    fig = figure()
    ax = fig.add_subplot(111)
    ax.plot(np.random.rand(10))
    def onclick(event):
        print('event.button=%d,  event.x=%d, event.y=%d, event.xdata=%f, \
        event.ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata))
    def oncpaint(event):
        ind=np.searchsorted(x,event.xdata)
        plt.title("You clicked index="+str(ind))
        #ax.plot([x[ind]],[y[ind]],".",color="red")
        fig.canvas.draw()

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    show()
