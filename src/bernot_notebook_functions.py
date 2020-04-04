from ipywidgets import interact, widgets
from IPython.display import display, Javascript
from bokeh.models import ColumnDataSource, SingleIntervalTicker
from bokeh.plotting import figure
from bokeh.io import push_notebook
from sympy.geometry import *
import typing
from typing import List
try:
    from src.bernot_calculations.bernot_subgraph import Bernot_Subgraph
    from src.bernot_calculations.bernot_graph import Bernot_Graph
    from src.bernot_calculations.node import Node, NodeType
except ImportError:
    import sys
    sys.path.insert(0,'./bernot_calculations/')
    from bernot_graph import Bernot_Graph
    from bernot_subgraph import Bernot_Subgraph
    from node import Node, NodeType

class BernotNotebook:
    MAX_POINT_VALUE = 10
    MIN_WIDGET_VALUE = 0
    STEP_WIDGET_VALUE = 0.1

    def __init__(self):
        pass

    def get_bounded_float_text_widget(self, value: float, maximum: float):
        return widgets.BoundedFloatText(
            value = value, min = BernotNotebook.MIN_WIDGET_VALUE, max = maximum, 
            step = BernotNotebook.STEP_WIDGET_VALUE, description = '', disabled = False)

    # https://github.com/minrk/ipython_extensions/blob/master/extensions/disable_autoscroll.py
    def get_string_to_set_autoscroll_to_false(self) -> str:
        return """
        IPython.OutputArea.prototype._should_scroll = function(lines) {
            return false;
        }
        """
        

    def get_source_number_slider(self):
        self.source_number = widgets.IntSlider(min=2, max=10, description="# Sources")
        return self.source_number

    def make_sources_tab(self):
        v = []
        for i in range(self.source_number.value):
            row_inputs = [widgets.IntText(description="X"), widgets.IntText(description="Y"), widgets.BoundedIntText(description="Weight", min=1)]
            v.append(widgets.HBox(row_inputs) )
        self.source_inputs = widgets.VBox(v)
        return self.source_inputs
        
    def make_sink_tab(self):
        self.sink_input = widgets.HBox([widgets.IntText(description="X"), widgets.IntText(description="Y")])
        return self.sink_input

    def make_parameters_tab(self):
        self.parameters_input = widgets.HBox([widgets.IntText(description="alpha")])
        return self.parameters_input

    def make_tabs(self):
        tab = widgets.Tab(children=[self.make_sources_tab(), self.make_sink_tab(), self.make_parameters_tab()])
        tab_titles = ["Sources", "Sink", "Parameters"]
        for i in range(len(tab_titles)):
            tab.set_title(i, tab_titles[i])
        return tab

    def get_source_list(self):
        self.source_list = []
        for i in range(len(self.source_inputs.children)):
            row = self.source_inputs.children[i]
            weight = row.children[2].value
            x = row.children[0].value
            y = row.children[1].value
            self.source_list.append(Node(weight, Point(x, y), NodeType.SOURCE))

    def get_sink(self):
        x = self.sink_input.children[0].value
        y = self.sink_input.children[1].value
        weight = 0
        for source in self.source_list:
            weight += source.weight
        self.sink = Node(weight, Point(x, y), NodeType.SINK)

    def get_parameters(self):
        self.alpha = self.parameters_input.children[0].value

    def check_valid_input(self):
        valid = True
        if (self.sink in self.source_list):
            widgets.Text("Error: sink is also a source")
            valid = False
        if (len(self.source_list) == len(set(self.source_list))):
            widgets.Text("Error: duplicate sources")
            valid = False
        if self.alpha <= 0 or self.alpha >= 1:
            widgets.Text("Error: invalid alpha")
            valid = False
        return valid

    def make_bernot_graph(self):
        self.get_source_list()
        self.get_sink()
        self.get_parameters()
        if check_valid_input():
            self.graph = Bernot_Graph(self.source_list, self.sink, self.alpha)
        
    def make_point_data(self):
        self.x_values = [self.graph.sink.point.x]
        self.y_values = [self.graph.sink.point.y]
        for key in self.graph.subgraph_map:
            subgraph: Bernot_Subgraph = self.graph.subgraph_map[key]
            nodes = [subgraph.source1, subgraph.source2, subgraph.pivot_node, subgraph.bifurcation]
            self.x_values.extend([n.point.x for n in nodes])
            self.y_values.extend([n.point.y for n in nodes])
        data = {"x_values": self.x_values, 'y_values': self.y_values}
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
            self.make_bernot_graph()
        self.make_point_data()
        fig = figure()
        fig.circle(x='x_values', y='y_values', source=self.point_source)
        fig.xaxis.ticker = SingleIntervalTicker(interval=1)
        fig.yaxis.ticker = SingleIntervalTicker(interval=1)
        delattr(self, "graph")
        return fig


    def get_output(self):
        self.output_text = widgets.Output(layout={'border': '1px solid black'})
        return self.output_text

    