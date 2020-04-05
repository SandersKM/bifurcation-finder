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

    def get_bounded_float_text_widget(self, value: float, maximum: float, dicription_text: str = ""):
        return widgets.BoundedFloatText(
            value = value, min = BernotNotebook.MIN_WIDGET_VALUE, max = maximum, 
            step = BernotNotebook.STEP_WIDGET_VALUE, description = dicription_text, disabled = False)

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
            row_inputs = [widgets.FloatText(description="X", value=i), widgets.FloatText(description="Y", value=3), widgets.BoundedFloatText(description="Weight", min=.001, value=1)]
            v.append(widgets.HBox(row_inputs) )
        self.source_inputs = widgets.VBox(v)
        return self.source_inputs
        
    def make_sink_tab(self):
        self.sink_input = widgets.HBox([widgets.FloatText(description="X", \
            value = float(self.source_number.value)/2),\
                 widgets.FloatText(description="Y", value = 0)])
        return self.sink_input

    def make_parameters_tab(self):
        self.parameters_input = widgets.HBox([widgets.BoundedFloatText(description="alpha", value=.5, max = .99, min = .001)])
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
        error_message = ""
        for i in range(len(self.source_list) - 1):
            if self.source_list[i] in self.source_list[i + 1:]:
                error_message += "Error: duplicate source " + str(self.source_list[i]) + "\n"
            if self.sink.point == self.source_list[i].point:
                error_message +="Error: sink is also a source\n"
        if self.alpha <= 0 or self.alpha >= 1:
            error_message +="Error: invalid alpha\n"
        return error_message

    def make_bernot_graph(self):
        self.get_source_list()
        self.get_sink()
        self.get_parameters()
        error_message = self.check_valid_input()
        if len(error_message) > 0:
            out = widgets.Output(layout={'border': '1px solid black'})
            out.append_stdout(error_message)
            return out
        self.graph = Bernot_Graph(self.source_list, self.sink, self.alpha)
        
    def make_point_data(self, nodes):
        x_values = []
        y_values = []
        size = []
        alpha = []
        color = []
        nodeType = []
        self.node_order = []
        for n in nodes:
            x_values.append(float(n.point.x))
            y_values.append(float(n.point.y))
            size.append(15)
            alpha.append(0.5)
            if n.node_type == NodeType.SOURCE:
                color.append("green")
            else:
                color.append("red")
            nodeType.append(n.node_type)
            self.node_order.append(n)
        data = {"x_values": x_values, 'y_values': y_values, \
            "color": color, "size": size, "alpha": alpha}
        self.point_source =  ColumnDataSource(data=data)

    def make_circle_data(self):
        self.circle_order = []
        data = {"x_values": [], 'y_values': [], "color": [], "radius": []}
        self.circle_source =  ColumnDataSource(data=data)

    def make_line_data(self):
        sink = self.graph.get_sink_point()
        x0 = [n.x for n in self.graph.get_source_points() + [sink]]
        y0 = [n.y for n in self.graph.get_source_points() + [sink]]
        x1 = [sink.x, sink.x, sink.x]
        y1 = [sink.y, sink.y, sink.y]
        segment_data = {"x0": x0, "y0": y0, "x1": x1, "y1": y1}

    def get_figure(self):
        fig = figure()
        self.make_point_data(self.graph.visualization_steps[0][1]["points"])
        fig.circle(x='x_values', y='y_values', size="size", color="color", alpha="alpha", source=self.point_source)
        self.make_circle_data()
        fig.ellipse(x="x_values", y="y_values", width="radius", height="radius",\
            color="color", fill_color=None, line_width=2, source=self.circle_source)
        fig.xaxis.ticker = SingleIntervalTicker(interval=1)
        fig.yaxis.ticker = SingleIntervalTicker(interval=1)
        return fig

    def get_output(self):
        self.output_text = widgets.Output(layout={'border': '1px solid black'})
        return self.output_text

    def update(self, step: int = 0):
        current_step = self.graph.visualization_steps[step]
        description = current_step[0]
        values = current_step[1]
        if len(values["circles"]) > 0:
            for circle in values["circles"]:
                if not circle in self.circle_order:
                    self.add_circle_to_circle_source(circle)
        self.update_circle_visibility()
        if description == 'get pivot' and not (values["points"][-1] in self.node_order):
            self.add_pivot_to_point_source(values["points"][-1])
        self.update_node_visibility((values["points"]))
        self.output_text.clear_output()
        self.output_text.append_stdout(description)
        push_notebook() 

    def update_circle_visibility(self, circles):
        for i in range(len(self.circle_order)):
            if self.circle_order[i] in circles:
                self.point_source.patch({"color": [(i, ["white"])]})
            else:
                self.point_source.patch({"color": [(i, ["white"])]})

    def add_circle_to_circle_source(self, circle: (Point, float)):
        self.circle_order.append(circle)
        self.circle_source.stream({"x_values": [circle[0].x], 'y_values': [circle[0].y],\
             "color": ["grey"], "radius": [circle[1]]})

    def update_node_visibility(self, nodes):
        for i in range(len(self.node_order)):
            if self.node_order[i] in nodes:
                self.point_source.patch({"alpha": [(i, [0.5])]})
            else:
                self.point_source.patch({"alpha": [(i, [0])]})

    def add_pivot_to_point_source(self, node: Node):
        self.node_order.append(node)
        self.point_source.stream({"color": ["purple"], "x_values": [float(node.point.x)],\
            "y_values": [float(node.point.y)], "alpha": [0.5], "size": [15]})
        

    