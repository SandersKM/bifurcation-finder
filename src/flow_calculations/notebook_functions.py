from ipywidgets import interact, widgets
from IPython.display import display, Javascript
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import push_notebook
import typing
from typing import List
try:
    from src.flow_calculations.point import Point
    from src.flow_calculations.nodes import Nodes
    from src.flow_calculations.node import Node
    from src.flow_calculations.flow import Flow
    from src.flow_calculations.flow_minimizer import FlowMinimizer
except ImportError:
    from point import Point
    from nodes import Nodes
    from node import Node
    from flow import Flow
    from flow_minimizer import FlowMinimizer


class Notebook:

    def __init__(self):
        pass

    def get_bounded_float_text_widget(self, value: float, maximum: float):
        minimum: float = 0
        step: float = 0.1
        return widgets.BoundedFloatText(value=value, min=minimum, max=maximum, step=step, description='', disabled=False)

    # https://github.com/minrk/ipython_extensions/blob/master/extensions/disable_autoscroll.py
    def get_string_to_set_autoscroll_to_false(self):
        return """
        IPython.OutputArea.prototype._should_scroll = function(lines) {
            return false;
        }
        """

    def get_accordion(self, children: List, titles: List):
        accordion = widgets.Accordion(children=children)
        for i in range(len(titles)):
            accordion.set_title(i, titles[i])
        return accordion

    def get_tab_children(self):
        tab_children = []
        point_labels = ["X", "Y"]
        self.w_source1x = self.get_bounded_float_text_widget(0.0, 10)
        self.w_source1y= self.get_bounded_float_text_widget(1.0, 10)
        tab_children.append(self.get_accordion([self.w_source1x, self.w_source1y], point_labels))
        self.w_source2x = self.get_bounded_float_text_widget(0.0, 10)
        self.w_source2y= self.get_bounded_float_text_widget(5.0, 10)
        tab_children.append(self.get_accordion([self.w_source2x, self.w_source2y], point_labels))
        self.w_sinkx = self.get_bounded_float_text_widget(4.0, 10)
        self.w_sinky = self.get_bounded_float_text_widget(3.0, 10)
        tab_children.append(self.get_accordion([self.w_sinkx, self.w_sinky], point_labels))
        self.w_h = self.get_bounded_float_text_widget(.001, .5)
        self.w_alpha = self.get_bounded_float_text_widget(.5, 1)
        self.max_steps = self.get_bounded_float_text_widget(100000, 10000000)
        self.min_diff = self.get_bounded_float_text_widget(.02, 1)
        tab_children.append(self.get_accordion([self.w_h, self.w_alpha, self.max_steps, self.min_diff], ["h", "alpha", "maximum steps", "stop distance"]))
        return tab_children

    def get_tab(self):
        tab = widgets.Tab(children=self.get_tab_children())
        tab_titles = ["Source 1", "Source 2", "Sink", "Parameters"]
        for i in range(len(tab_titles)):
            tab.set_title(i, tab_titles[i])
        return tab

    def make_network(self):
        self.nodes = Nodes()
        self.nodes.addSource(Node(1,Point(self.w_source1x.value, self.w_source1y.value)))
        self.nodes.addSource(Node(1,Point(self.w_source2x.value, self.w_source2y.value)))
        self.nodes.addSink(Node(2, Point(self.w_sinkx.value, self.w_sinky.value)))
        self.nodes.addBifurcation(Point(self.w_sinkx.value, self.w_sinky.value)) 

    def get_flow(self):
        self.make_network()
        return Flow(self.w_h.value, self.w_alpha.value, self.nodes)

    def make_steps(self):
        flow_minimizer = FlowMinimizer(self.get_flow(), self.max_steps.value, self.min_diff.value)
        flow_minimizer.get_minimum_flow()
        self.steps = flow_minimizer.steps
        self.theta = flow_minimizer.theta
        self.cost = flow_minimizer.cost

    def make_point_data(self):
        self.x_values = [n.getX() for n in  self.nodes.getSourcePoints() + self.nodes.getSinkPoints() + self.nodes.getSinkPoints() ]
        y_values = [n.getY() for n in  self.nodes.getSourcePoints() + self.nodes.getSinkPoints() + self.nodes.getSinkPoints() ]
        data = {"x_values": self.x_values, 'y_values': y_values}
        self.point_source =  ColumnDataSource(data=data)

    def make_line_data(self):
        x0 = [n.getX() for n in self.nodes.getSourcePoints() + self.nodes.getSinkPoints()]
        y0 = [n.getY() for n in self.nodes.getSourcePoints() + self.nodes.getSinkPoints()]
        x1 = [self.nodes.getSinkPoints()[0].getX(), self.nodes.getSinkPoints()[0].getX(), self.nodes.getSinkPoints()[0].getX()]
        y1 = [self.nodes.getSinkPoints()[0].getY(), self.nodes.getSinkPoints()[0].getY(), self.nodes.getSinkPoints()[0].getY()]
        segment_data = {"x0": x0, "y0": y0, "x1": x1, "y1": y1}
        self.segment_source =  ColumnDataSource(data=segment_data)

    def get_figure(self):
        self.make_steps()
        self.make_line_data()
        self.make_point_data()
        fig = figure()
        fig.circle(x='x_values', y='y_values', source=self.point_source)
        fig.segment(x0 = "x0", y0="y0", x1="x1", y1="y1", color="navy", line_width=3, source=self.segment_source)
        return fig

    def get_output(self):
        self.output_text = widgets.Output(layout={'border': '1px solid black'})
        return self.output_text

    def update(self, step: int = 0):
        current_step = self.steps[step]
        self.point_source.patch({"x_values": [(len(self.x_values)-1, current_step)]})
        self.segment_source.patch({"x1": [(slice(3), [current_step, current_step, current_step])]})
        self.output_text.clear_output()
        self.output_text.append_stdout(f"Theta: {self.theta[step]}\t Cost: {self.cost[step]}")
        push_notebook() 
