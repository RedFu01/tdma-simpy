import matplotlib.pyplot as plt

class Plotter(object):
    def plot_time_series(self, x, y, label, name):
        fig = plt.figure()
        plt.plot(x, y)
        plt.xlabel('t')
        plt.ylabel(label)
        fig.tight_layout()
        fig.set_size_inches((4.7, 3.5), forward=False)
        fig.savefig(f"./figures/{name}.png", dpi=500, bbox_inches='tight', pad_inches=0.01)

    def plot_histogram(self, data, name):
        fig = plt.figure()
        plt.hist(data, 50)
        fig.tight_layout()
        fig.set_size_inches((4.7, 3.5), forward=False)
        fig.savefig(f"./figures/{name}.png", dpi=500, bbox_inches='tight', pad_inches=0.01)
        plt.close()
