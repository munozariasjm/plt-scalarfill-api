# Plotting wrapper for echarts to make
# a bit more pythonic and easier to use.
# by: Jose M Munoz @munozariasjm

import pyecharts.options as opts
from pyecharts.charts import Line
from streamlit_echarts import st_pyecharts
import pandas as pd


class TimeLinePlotterTool:
    def __init__(
        self, title="", subtitle="", x_axis_name="", y_axis_name="", figsize=None
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.x_axis_name = x_axis_name
        self.y_axis_name = y_axis_name

    def set(
        self, *, title="", subtitle="", x_axis_name="", y_axis_name="",
    ):
        self.title = title
        self.subtitle = subtitle
        self.x_axis_name = x_axis_name
        self.y_axis_name = y_axis_name

    def timeplot(self, data: pd.DataFrame, time_axis="dt", *, cols=None):
        try:
            assert time_axis in data.columns, "Time axis not found in df"
            time_axis = data[time_axis].tolist()
        except Exception as e:
            print(e)
            time_axis = data.index.tolist()
        t_axis_data = time_axis  # .strftime("%B %d, %Y, %r")
        if cols is None:
            cols = [c for c in data.columns if c != time_axis]

        line = self.plot_space(t_axis_data)
        for col in cols:
            line = self._add_line(line, data[col], col)

        line.set_global_opts(
            title_opts=opts.TitleOpts(title=self.title, subtitle=self.subtitle),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True, item_size=10, item_gap=5,),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
        b = line
        st_pyecharts(b)

    def plot_space(self, x_axis_data: list, figsize=None):
        if figsize:
            assert isinstance(figsize, tuple), "figsize must be a tuple"
            _figsize = figsize
        else:
            _figsize = (16, 8)
        line = Line(
            init_opts=opts.InitOpts(
                width=f"{_figsize[0]*100}px", height=f"{_figsize[1]*100}px"
            )
        )
        line.add_xaxis(xaxis_data=x_axis_data)
        return line

    def _add_line(self, line: Line, y: list, name: str) -> Line:
        _line = line.add_yaxis(
            name,
            y,
            symbol_size=8,
            is_hover_animation=False,
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=1.5),
            is_smooth=True,
        )
        return _line
