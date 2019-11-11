from ipywidgets import interact, widgets
from IPython.display import display
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import push_notebook
import typing
from typing import List
from point import Point
from network import Network
from node import Node
from flow import Flow
from flow_minimizer import FlowMinimizer


class Notebook:

    def get_bounded_float_text_widget(self, value: float, maximum: float):
        minimum: float = 0
        step: float = 0.1
        return widgets.BoundedFloatText(value=value, min=minimum, max=maximum, step=step, description='', disabled=False)

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
        self.min_diff = self.get_bounded_float_text_widget(.0000001, 1)
        tab_children.append(self.get_accordion([self.w_h, self.w_alpha, self.max_steps, self.min_diff], ["h", "alpha", "maximum steps", "stop distance"]))
        return tab_children

    def get_tab(self):
        tab = widgets.Tab(children=self.get_tab_children())
        tab_titles = ["Source 1", "Source 2", "Sink", "Parameters"]
        for i in range(len(tab_titles)):
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

    def make_steps(self):
        self.steps = FlowMinimizer().get_flow_steps(self.make_flow(), self.max_steps.value, self.min_diff.value)

    def make_point_data(self):
        self.x_values = [n.getX() for n in  self.network.getSourcePoints() + self.network.getSinkPoints() + self.network.getSinkPoints() ]
        y_values = [n.getY() for n in  self.network.getSourcePoints() + self.network.getSinkPoints() + self.network.getSinkPoints() ]
        data = {"x_values": self.x_values, 'y_values': y_values}
        self.point_source =  ColumnDataSource(data=data)

    def make_line_data(self):
        x0 = [n.getX() for n in self.network.getSourcePoints() + self.network.getSinkPoints()]
        y0 = [n.getY() for n in self.network.getSourcePoints() + self.network.getSinkPoints()]
        x1 = [self.network.getSinkPoints()[0].getX(), self.network.getSinkPoints()[0].getX(), self.network.getSinkPoints()[0].getX()]
        y1 = [self.network.getSinkPoints()[0].getY(), self.network.getSinkPoints()[0].getY(), self.network.getSinkPoints()[0].getY()]
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

    def update(self, step: int = 0):
        current_step = self.steps[step]
        self.point_source.patch({"x_values": [(len(self.x_values)-1, current_step)]})
        self.segment_source.patch({"x1": [(slice(3), [current_step, current_step, current_step])]})
        push_notebook() 
