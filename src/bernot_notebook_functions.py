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
    from src.bernot_calculations.node import Noed
except ImportError:
    import sys
    sys.path.insert(0,'./bernot_calculations/')
    from bernot_graph import Bernot_Graph
    from bernot_subgraph import Bernot_Subgraph
    from node import Node

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

    def get_source_input_box(self):
        v = []
        for i in range(self.source_number.value):
            row_inputs = [widgets.IntText(description="X"), widgets.IntText(description="Y"), widgets.BoundedIntText(description="Weight", min=1)]
            v.append(widgets.HBox(row_inputs) )
        self.source_inputs = widgets.VBox(v)
        return self.source_inputs

    def make_source_list(self):
        self.source_list = []
        for i in range(len(self.source_inputs)):
            row = self.source_inputs.children[i]
            weight = row.children[2].value
            x = row.children[0].value
            y = row.children[1].value
            self.source_list.append(Node(weight, Point(x, y)))
        
    