
from avi.log import logger

from avi.utils.plotter import save_plot
from avi.utils.data.data_file import data_file as data

class dummy:
    param1 = 0
    param2 = 0
    gaia_table = ""
    str_data = ""
    res = 0
    def run(self, id):
        from bokeh.plotting import figure
        x = [1,2,3,4,5,7, int(self.param1)]
        y = [6,7,2,4,5,4, int(self.param2)]
        plot = figure(title="simple", x_axis_label='x',y_axis_label='y')
        plot.line(x,y, legend="temp", line_width = 2)
        save_plot(id, "dummy", plot)
        x = [int(self.param1),int(self.param1)+int(self.param2)]
        y = [int(self.param2),int(self.param1)+int(self.param2)]
        plot = figure(title="simple", x_axis_label='x',y_axis_label='y')
        plot.line(x,y, legend="temp", line_width = 2)
        save_plot(id, "dummy", plot)
        f = data(id).file("result")
        f.write("pruebaaa")
        f.write(str(x))
        f.write(str(y))
        f.close()
