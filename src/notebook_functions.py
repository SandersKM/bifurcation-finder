from ipywidgets import interact, widgets
from IPython.display import display
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
import typing
from typing import List
from flow_calculations.point import Point
from flow_calculations.network import Network
from flow_calculations.node import Node
from flow_calculations.flow import Flow
from flow_calculations.flow_minimizer import FlowMinimizer


class Notebook:

    def make_bounded_float_text_widget(self, value: float, maximum: float):
        minimum: float = 0
        step: float = 0.1
        return widgets.BoundedFloatText(value=value, min=minimum, max=maximum, step=step, description='', disabled=False)

    def make_accordion(self, children: List, titles: List):
        accordion = widgets.Accordion(children=children)
        for i in range(len(titles)):
            accordion.set_title(i, titles[i])
        return accordion

    def get_tab_children(self):
        tab_children = []
        point_labels = ["X", "Y"]
        self.w_source1x = self.make_bounded_float_text_widget(0.0, 10)
        self.w_source1y= self.make_bounded_float_text_widget(1.0, 10)
        tab_children.append(self.make_accordion([self.w_source1x, self.w_source1y], point_labels))
        self.w_source2x = self.make_bounded_float_text_widget(0.0, 10)
        self.w_source2y= self.make_bounded_float_text_widget(5.0, 10)
        tab_children.append(self.make_accordion([self.w_source2x, self.w_source2y], point_labels))
        self.w_sinkx = self.make_bounded_float_text_widget(4.0, 10)
        self.w_sinky = self.make_bounded_float_text_widget(3.0, 10)
        tab_children.append(self.make_accordion([self.w_sinkx, self.w_sinky], point_labels))
        self.w_h = self.make_bounded_float_text_widget(.001, .5)
        self.w_alpha = self.make_bounded_float_text_widget(.5, 1)
        self.max_steps = self.make_bounded_float_text_widget(100000, 10000000)
        self.min_diff = self.make_bounded_float_text_widget(.0000001, 1)
        tab_children.append(self.make_accordion([self.w_h, self.w_alpha, self.max_steps, self.min_diff], ["h", "alpha", "maximum steps", "stop distance"]))
        return tab_children

    def make_tab(self):
        tab = widgets.Tab(children=self.get_tab_children())
        tab_titles = ["Source 1", "Source 2", "Sink", "Parameters"]
        for i in len(range(tab_titles)):
            tab.set_title(i, tab_titles[i])
        return tab

    def make_network(self):
        self.network = Network()
        self.network.addSource(Node(1,Point(self.w_source1x.value, self.w_source1y.value)))
        self.network.addSource(Node(1,Point(self.w_source2x.value, self.w_source2y.value)))
        self.network.addSink(Node(2, Point(self.w_sinkx.value, self.w_sinky.value)))
        self.network.addBifurcation(Point(self.w_sinkx.value, self.w_sinky.value)) 

    def make_flow(self):
        self.make_network()
        return Flow(self.w_h.value, self.w_alpha.value, self.network)

    def get_steps(self):
        return FlowMinimizer(self.make_flow(), self.max_steps.value, self.min_diff.value)

    def get_point_data(self):
        x_values = [n.getX() for n in  self.network.getSourcePoints() + self.network.getSinkPoints() + self.network.getSinkPoints() ]
        y_values = [n.getY() for n in  self.network.getSourcePoints() + self.network.getSinkPoints() + self.network.getSinkPoints() ]
        data = {"x_values": x_values, 'y_values': y_values}
        return ColumnDataSource(data=data)

    def get_line_data(self):
        x0 = [n.getX() for n in self.network.getSourcePoints() + self.network.getSinkPoints()]
        y0 = [n.getY() for n in self.network.getSourcePoints() + self.network.getSinkPoints()]
        x1 = [self.network.getSinkPoints()[0].getX() + self.network.getSinkPoints()[0].getX() + self.network.getSinkPoints()[0].getX()]
        y1 = [self.network.getSinkPoints()[0].getY() + self.network.getSinkPoints()[0].getY() + self.network.getSinkPoints()[0].getY()]
        segment_data = {"x0": x0, "y0": y0, "x1": x1, "y1": y1}
        return ColumnDataSource(data=segment_data)

    def get_figure(self):
        fig = figure()
        fig.circle(x='x_values', y='y_values', source=self.get_point_data())
        fig.segment(x0 = "x0", y0="y0", x1="x1", y1="y1", color="navy", line_width=3, source=self.get_line_data())
        return fig
