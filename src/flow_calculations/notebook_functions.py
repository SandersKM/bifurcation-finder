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
    from src.flow_calculations.node import Node
    from src.flow_calculations.network import Network
    from src.flow_calculations.flow import Flow
except ImportError:
    from point import Point
    from vertices import Vertices
    from node import Node
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
        point_labels = ["X", "Y"]
        self.w_source1x = self.get_bounded_float_text_widget(0.0, Notebook.MAX_POINT_VALUE)
        self.w_source1y= self.get_bounded_float_text_widget(1.0, Notebook.MAX_POINT_VALUE)
        tab_children.append(self.get_accordion([self.w_source1x, self.w_source1y], point_labels))
        self.w_source2x = self.get_bounded_float_text_widget(0.0, Notebook.MAX_POINT_VALUE)
        self.w_source2y= self.get_bounded_float_text_widget(5.0, Notebook.MAX_POINT_VALUE)
        tab_children.append(self.get_accordion([self.w_source2x, self.w_source2y], point_labels))
        self.w_sinkx = self.get_bounded_float_text_widget(4.0, Notebook.MAX_POINT_VALUE)
        self.w_sinky = self.get_bounded_float_text_widget(3.0, Notebook.MAX_POINT_VALUE)
        tab_children.append(self.get_accordion([self.w_sinkx, self.w_sinky], point_labels))
        self.w_h = self.get_bounded_float_text_widget(.2, .5)
        self.w_alpha = self.get_bounded_float_text_widget(.5, 1)
        self.max_steps = self.get_bounded_float_text_widget(100000, 10000000)
        self.min_diff = self.get_bounded_float_text_widget(.02, 1)
        tab_children.append(self.get_accordion(
            [self.w_h, self.w_alpha, self.max_steps, self.min_diff], 
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
        self.vertices.add_source(Node(1,Point(self.w_source1x.value, self.w_source1y.value)))
        self.vertices.add_source(Node(1,Point(self.w_source2x.value, self.w_source2y.value)))
        self.vertices.add_sink(Node(2, Point(self.w_sinkx.value, self.w_sinky.value)))
        self.vertices.add_bifurcation(Point(self.w_sinkx.value, self.w_sinky.value)) 
        return Network(self.w_h.value, self.w_alpha.value, self.vertices)        

    def make_steps(self):
        flow = Flow(self.get_network(), self.max_steps.value, self.min_diff.value)
        flow.get_flow()
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
        return fig

    def get_optimal_bifurcation_point(self):
        self.make_steps()
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
