from ipywidgets import interact, widgets
from IPython.display import display, Javascript
from bokeh.models import ColumnDataSource, SingleIntervalTicker
from bokeh.plotting import figure
from bokeh.io import push_notebook
import typing
from typing import List
try:
    from src.flow_calculations.point import Point
    from src.flow_calculations.graph import Graph
    from src.flow_calculations.node import Node, NodeType
    from src.flow_calculations.network import Network
    from src.flow_calculations.flow import Flow
except ImportError:
    import sys
    sys.path.insert(0,'./flow_calculations/')
    from point import Point
    from graph import Graph
    from node import Node, NodeType
    from network import Network
    from flow import Flow

class FlowNotebook:
    MAX_POINT_VALUE = 10
    MIN_WIDGET_VALUE = 0
    STEP_WIDGET_VALUE = 0.1

    def __init__(self):
        pass

    def get_bounded_float_text_widget(self, value: float, maximum: float):
        return widgets.BoundedFloatText(
            value = value, min = FlowNotebook.MIN_WIDGET_VALUE, max = maximum, 
            step = FlowNotebook.STEP_WIDGET_VALUE, description = '', disabled = False)

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
        self.source_1_x = self.get_bounded_float_text_widget(0.0, FlowNotebook.MAX_POINT_VALUE)
        self.source_1_y= self.get_bounded_float_text_widget(1.0, FlowNotebook.MAX_POINT_VALUE)
        self.source_1_weight = widgets.BoundedFloatText(value = 1.0, min = 0.1, step = 0.1)
        tab_children.append(self.get_accordion([self.source_1_x, self.source_1_y, self.source_1_weight], point_labels))
        self.source_2_x = self.get_bounded_float_text_widget(0.0, FlowNotebook.MAX_POINT_VALUE)
        self.source_2_y= self.get_bounded_float_text_widget(5.0, FlowNotebook.MAX_POINT_VALUE)
        self.source_2_weight = widgets.BoundedFloatText(value = 1.0, min = 0.1, step = 0.1)
        tab_children.append(self.get_accordion([self.source_2_x, self.source_2_y, self.source_2_weight], point_labels))
        self.sink_x = self.get_bounded_float_text_widget(4.0, FlowNotebook.MAX_POINT_VALUE)
        self.sink_y = self.get_bounded_float_text_widget(3.0, FlowNotebook.MAX_POINT_VALUE)
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
        self.graph = Graph()
        source1 = Node(self.source_1_weight.value, Point(self.source_1_x.value, self.source_1_y.value), NodeType.SOURCE)
        source2 = Node(self.source_2_weight.value, Point(self.source_2_x.value, self.source_2_y.value), NodeType.SOURCE)
        sink = Node((self.source_1_weight.value + self.source_2_weight.value), Point(self.sink_x.value, self.sink_y.value), NodeType.SINK)
        bifurcation = Node(0, Point(self.sink_x.value, self.sink_y.value), NodeType.BIFURCATION)
        self.graph.add_node(source1)
        self.graph.add_node(source2)
        self.graph.add_node(sink)
        self.graph.add_node(bifurcation)
        self.graph.add_edge(source1, bifurcation)
        self.graph.add_edge(source2, bifurcation)
        self.graph.add_edge(bifurcation, sink)
        return Network(self.h.value, self.alpha.value, self.graph)        

    def make_steps(self, verbose=False):
        flow = Flow(self.get_network(), self.max_steps.value, self.min_diff.value)
        flow.get_flow(verbose)
        self.steps = flow.steps
        self.theta = flow.theta
        self.cost = flow.cost
        self.m_alpha = flow.m_alpha

    def make_point_data(self):
        self.x_values = [
            n.x for n in self.graph.get_source_points() + [self.graph.get_sink_point()]
            + [self.graph.get_sink_point()] ]
        self.y_values = [
            n.y for n in self.graph.get_source_points() + [self.graph.get_sink_point()]
            + [self.graph.get_sink_point()] ]
        colors = ["green", "green", "red", "blue"]
        legend = ["source", "source", "sink", "bifurcation"]
        data = {"x_values": self.x_values, 'y_values': self.y_values, "colors": colors, "legend": legend}
        self.point_source =  ColumnDataSource(data=data)

    def make_line_data(self):
        sink = self.graph.get_sink_point()
        x0 = [n.x for n in self.graph.get_source_points() + [sink]]
        y0 = [n.y for n in self.graph.get_source_points() + [sink]]
        x1 = [sink.x, sink.x, sink.x]
        y1 = [sink.y, sink.y, sink.y]
        segment_data = {"x0": x0, "y0": y0, "x1": x1, "y1": y1}
        self.segment_source =  ColumnDataSource(data=segment_data)

    def get_figure(self):
        if not hasattr(self, "graph"):
            self.get_optimal_bifurcation_point()
        self.make_line_data()
        self.make_point_data()
        fig = figure(match_aspect=True)
        try:
            fig.circle(x='x_values', y='y_values', color='colors', size=15, alpha=0.8, legend_group='legend', source=self.point_source)
        except:
            fig.circle(x='x_values', y='y_values', color='colors', size=15, alpha=0.8, source=self.point_source)
        fig.segment(x0 = "x0", y0="y0", x1="x1", y1="y1", color="navy", line_width=3, source=self.segment_source)
        fig.xaxis.ticker = SingleIntervalTicker(interval=1)
        fig.yaxis.ticker = SingleIntervalTicker(interval=1)
        delattr(self, "graph")
        return fig

    def get_optimal_bifurcation_point(self, verbose=False):
        self.make_steps(verbose)
        out = widgets.Output(layout={'border': '1px solid black'})
        current_step = self.steps[-1]
        out.append_stdout(f'Location:  ({round(current_step.x, 3)}, {round(current_step.y,3)}) \t'\
            + f' M alpha: {round(self.m_alpha[-1], 3)}\t Total Cost: {round(self.cost[-1])} \t Theta: {round(self.theta[-1])}')
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
        self.output_text.append_stdout(f"Theta: {round(self.theta[step], 3)}\t M alpha: {round(self.m_alpha[step], 3)}"\
            + f"\t Total Cost: {round(self.cost[step],3)}\t Location: ({round(current_step.x, 3)}, {round(current_step.y,3)})")
        push_notebook() 
