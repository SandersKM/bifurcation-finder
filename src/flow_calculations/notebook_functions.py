from ipywidgets import interact, widgets
from IPython.display import display, Javascript
from bokeh.models import ColumnDataSource, SingleIntervalTicker
from bokeh.plotting import figure
from bokeh.io import push_notebook
import typing
from typing import List
try:
    from src.flow_calculations.point import Point
    from src.flow_calculations.vertices import Vertices
    from src.flow_calculations.node import Node, NodeType
    from src.flow_calculations.network import Network
    from src.flow_calculations.flow import Flow
except ImportError:
    from point import Point
    from vertices import Vertices
    from node import Node, NodeType
    from network import Network
    from flow import Flow

class Notebook:
    MAX_POINT_VALUE = 10
    MIN_WIDGET_VALUE = 0
    STEP_WIDGET_VALUE = 0.1

    def __init__(self):
        pass

    def get_bounded_float_text_widget(self, value: float, maximum: float):
        return widgets.BoundedFloatText(
            value = value, min = Notebook.MIN_WIDGET_VALUE, max = maximum, 
            step = Notebook.STEP_WIDGET_VALUE, description = '', disabled = False)

    # https://github.com/minrk/ipython_extensions/blob/master/extensions/disable_autoscroll.py
    def get_string_to_set_autoscroll_to_false(self) -> str:
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
        point_labels = ["X", "Y", "Weight"]
        self.source_1_x = self.get_bounded_float_text_widget(0.0, Notebook.MAX_POINT_VALUE)
        self.source_1_y= self.get_bounded_float_text_widget(1.0, Notebook.MAX_POINT_VALUE)
        self.source_1_weight = widgets.BoundedFloatText(value = 1.0, min = 0.1, step = 0.1)
        tab_children.append(self.get_accordion([self.source_1_x, self.source_1_y, self.source_1_weight], point_labels))
        self.source_2_x = self.get_bounded_float_text_widget(0.0, Notebook.MAX_POINT_VALUE)
        self.source_2_y= self.get_bounded_float_text_widget(5.0, Notebook.MAX_POINT_VALUE)
        self.source_2_weight = widgets.BoundedFloatText(value = 1.0, min = 0.1, step = 0.1)
        tab_children.append(self.get_accordion([self.source_2_x, self.source_2_y, self.source_2_weight], point_labels))
        self.sink_x = self.get_bounded_float_text_widget(4.0, Notebook.MAX_POINT_VALUE)
        self.sink_y = self.get_bounded_float_text_widget(3.0, Notebook.MAX_POINT_VALUE)
        tab_children.append(self.get_accordion([self.sink_x, self.sink_y], point_labels))
        self.h = self.get_bounded_float_text_widget(.2, .5)
        self.alpha = self.get_bounded_float_text_widget(.5, 1)
        self.max_steps = self.get_bounded_float_text_widget(100000, 10000000)
        self.min_diff = self.get_bounded_float_text_widget(0.000001, 1)
        tab_children.append(self.get_accordion(
            [self.h, self.alpha, self.max_steps, self.min_diff], 
            ["h", "alpha", "maximum steps", "stop distance"]))
        return tab_children

    def get_tab(self):
        tab = widgets.Tab(children=self.get_tab_children())
        tab_titles = ["Source 1", "Source 2", "Sink", "Parameters"]
        for i in range(len(tab_titles)):
            tab.set_title(i, tab_titles[i])
        return tab

    def get_network(self):
        self.vertices = Vertices()
        self.vertices.add_source(Node(self.source_1_weight.value, Point(self.source_1_x.value, self.source_1_y.value)))
        self.vertices.add_source(Node(self.source_2_weight.value, Point(self.source_2_x.value, self.source_2_y.value)))
        self.vertices.add_sink(Node(
            (self.source_1_weight.value + self.source_2_weight.value), Point(self.sink_x.value, self.sink_y.value)))
        self.vertices.add_bifurcation(Point(self.sink_x.value, self.sink_y.value)) 
        return Network(self.h.value, self.alpha.value, self.vertices)        

    def make_steps(self, verbose=False):
        flow = Flow(self.get_network(), self.max_steps.value, self.min_diff.value)
        flow.get_flow(verbose)
        self.steps = flow.steps
        self.theta = flow.theta
        self.cost = flow.cost

    def make_point_data(self):
        self.x_values = [
            n.x for n in self.vertices.get_source_points() + self.vertices.get_sink_points()
            + self.vertices.get_sink_points() ]
        self.y_values = [
            n.y for n in self.vertices.get_source_points() + self.vertices.get_sink_points()
            + self.vertices.get_sink_points() ]
        data = {"x_values": self.x_values, 'y_values': self.y_values}
        self.point_source =  ColumnDataSource(data=data)

    def make_line_data(self):
        x0 = [n.x for n in self.vertices.get_source_points() + self.vertices.get_sink_points()]
        y0 = [n.y for n in self.vertices.get_source_points() + self.vertices.get_sink_points()]
        x1 = [self.vertices.get_sink_points()[0].x, self.vertices.get_sink_points()[0].x, self.vertices.get_sink_points()[0].x]
        y1 = [self.vertices.get_sink_points()[0].y, self.vertices.get_sink_points()[0].y, self.vertices.get_sink_points()[0].y]
        segment_data = {"x0": x0, "y0": y0, "x1": x1, "y1": y1}
        self.segment_source =  ColumnDataSource(data=segment_data)

    def get_figure(self):
        if not hasattr(self, "vertices"):
            self.get_optimal_bifurcation_point()
        self.make_line_data()
        self.make_point_data()
        fig = figure()
        fig.circle(x='x_values', y='y_values', source=self.point_source)
        fig.segment(x0 = "x0", y0="y0", x1="x1", y1="y1", color="navy", line_width=3, source=self.segment_source)
        fig.xaxis.ticker = SingleIntervalTicker(interval=1)
        fig.yaxis.ticker = SingleIntervalTicker(interval=1)
        delattr(self, "vertices")
        return fig

    def get_optimal_bifurcation_point(self, verbose=False):
        self.make_steps(verbose)
        out = widgets.Output(layout={'border': '1px solid black'})
        out.append_stdout(f'Location: {self.steps[-1]} \t Cost: {self.cost[-1]} \t Theta: {self.theta[-1]}')
        return out

    def get_output(self):
        self.output_text = widgets.Output(layout={'border': '1px solid black'})
        return self.output_text

    def update(self, step: int = 0):
        current_step = self.steps[step]
        self.point_source.patch({"x_values": [(len(self.x_values)-1, current_step.x)]})
        self.point_source.patch({"y_values": [(len(self.y_values)-1, current_step.y)]})
        self.segment_source.patch({"x1": [(slice(3), [current_step.x, current_step.x, current_step.x])]})
        self.segment_source.patch({"y1": [(slice(3), [current_step.y, current_step.y, current_step.y])]})
        self.output_text.clear_output()
        self.output_text.append_stdout(f"Theta: {self.theta[step]}\t Cost: {self.cost[step]}\t Location: {current_step}")
        push_notebook() 
