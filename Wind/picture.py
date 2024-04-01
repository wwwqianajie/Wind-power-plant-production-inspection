import random
import matplotlib.pyplot as plt

class LiveGraph:
    def __init__(self):
        # Create empty lists for x and y data
        self.xdata = list(range(50))
        self.ydata = [0] * 50

        # Create a figure and axis
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot(self.xdata, self.ydata)

        # Set up timer for periodic updates
        self.timer = self.fig.canvas.new_timer(interval=100)
        self.timer.add_callback(self.update_graph)
        self.timer.start()

    def update_graph(self):
        # Update data
        self.ydata = self.ydata[1:] + [random.randint(0, 10)]

        # Update the plot
        self.line.set_ydata(self.ydata)
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()

    def run(self):
        # Enable interactive mode
        plt.ion()

        # Show the plot
        plt.show()

live_graph = LiveGraph()
live_graph.run()