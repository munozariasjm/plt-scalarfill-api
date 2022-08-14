# Plotting wrapper for echarts to make
# a bit more pythonic and easier to use.
# by: Jose M Munoz @munozariasjm

from distutils.command.install_egg_info import install_egg_info
from re import sub
import pyecharts.options as opts
from pyecharts.charts import Line
import pyecharts
from streamlit_echarts import st_pyecharts
import pandas as pd
from dataclasses import dataclass
from typing import Tuple


@dataclass
class TimeLinePlotterTool:
    """Simple plotting wrappler for interactive timeseries visualizations using a
    pythonic api. All the plotting interface is designed for streamlit, but the 
    when pyecharts is working, can work in any evironment.
    """
    title: str = "",
    subtitle: str = "",
    x_axis_label: str = "x",
    y_axis_label: str = "y",

    @classmethod
    def set(clf, ax=None, *, x_label=None, y_label=None, subtitle=None):
        """Setter for some characteristics of the plot space

        Args:
            title (str, optional): Title to put on the figure. Defaults to "".
            subtitle (str, optional): Subtitle of the figure. Defaults to "".
            x_axis_label (str, optional): Label to put in the x axis. Defaults to "".
            y_axis_label (str, optional): Label to put in the y axis. Defaults to "".
        """
        if subtitle:
            clf.subtitle = subtitle
        elif x_label:
            clf.x_axis_label = x_label
        elif y_label:
            clf.y_axis_label = y_label
            
        
    @classmethod
    def subplots(cls, size: Tuple[int],
                 figsizes: Tuple[tuple] = None) -> tuple:
        """A little wrappler that imitates the basic behaveur of plt.subplots"""
        fig = cls()
        if not isinstance(size, (tuple, list)):
            if isinstance(size, int):
                n_rows = size
                n_cols = 1
            else:
                print("Specify the configuration as (nrows, ncols)")
                raise TypeError
        n_rows = size[0]
        n_cols = size[1]
        if not figsizes or not isinstance(figsizes, (tuple, list)):
            figsizes = [[None for j in range(n_rows)] for i in range(n_cols)]
        ax = []
        for i in range(n_cols):
            ax.append([fig._get_line(figsizes[i][j])
                        for j in range(n_rows)])
        print(ax)
        if n_cols == 1:
            return fig, ax[0]
        else: 
            return fig, ax
        
    @staticmethod
    def _get_line(figsize):
        if figsize:
            assert isinstance(figsize, tuple), "figsize must be a tuple."
            _figsize = figsize
        else:
            _figsize = (16, 8)
        line = Line(init_opts=opts.InitOpts(
                    width=f"{_figsize[0]*100}px",
                    height=f"{_figsize[1]*100}px"
                )
            )
        return line

    def _lineplot_df(self, data: pd.DataFrame, x="dt", cols=None, ax=None):
        try:
            assert x in data.columns, "The x axis not found in df"
            time_axis = data[x].tolist()
        except Exception as e:
            print(e)
            time_axis = data.index.tolist()
        t_axis_data = time_axis
        if cols is None:
            cols = [c for c in data.columns if c != time_axis]
        line = self.plot_space(t_axis_data, line=ax)
        for col in cols:
            line = self._add_line(line, data[col], col)
        return line

    def set_title(self, title: str):
        self.title = title
    
    def lineplot(self, data: pd.DataFrame = None, x="dt", *, y=None, ax=None, show=False):
        """Plotter for time series using a seaborn-like style with a dataframe

        Args:
            data (pd.DataFrame): _description_
            time_axis (str, optional): _description_. Defaults to "dt".
            cols (_type_, optional): _description_. Defaults to None.
        """
        if isinstance(x, str):
            line = self._lineplot_df(data, x, cols=y)

        line.set_global_opts(
            title_opts=opts.TitleOpts(title=self.title, subtitle=self.subtitle),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True, link=[{"xAxisIndex": "all"}]
            ),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=True,
                    is_realtime=True,
                    start_value=30,
                    end_value=70,
                    xaxis_index=[0, 1],
                )
            ],
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=True),
            ),
            legend_opts=opts.LegendOpts(pos_left="center"),
            toolbox_opts=opts.ToolboxOpts(
                is_show=True,
                item_size=10,
                item_gap=5,
                feature={
                    "dataZoom": {"yAxisIndex": "none"},
                    "restore": {},
                    "saveAsImage": {},
                },
            ),
        )
        b = line
        if show:
            self.st_show(b)
        return b
    
    @staticmethod
    def st_show(ax) -> None:
        if not isinstance(ax, (list, tuple)):
            try:
                st_pyecharts(ax)
            except Exception as e:
                print("Could not display in streamlit")
                print(e)
        else:
            for j, col in enumerate(ax):
                for i, line in enumerate(col):
                    st_pyecharts(line)
        
    @staticmethod
    def py_show(ax) -> None:
        # TODO
        raise NotImplementedError

    def plot_space(self, x_axis_data: list, figsize=None, line=None):
        if not line:
            line = self._get_line(figsize)
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

ech_plotter = TimeLinePlotterTool()