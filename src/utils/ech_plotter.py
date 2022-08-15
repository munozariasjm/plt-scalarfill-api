# Plotting wrapper for echarts to make
# a bit more pythonic and easier to use.
# by: Jose M Munoz @munozariasjm

from pyecharts.options.global_options import *
from distutils.command.install_egg_info import install_egg_info
from re import sub
import pyecharts.options as opts
from pyecharts.charts import Line
import pyecharts
from streamlit_echarts import st_pyecharts
import pandas as pd
from dataclasses import dataclass
from typing import Tuple
import streamlit as st

@dataclass
class LinePlotterTool:
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
        if isinstance(cols, str):
            cols = [cols]
        elif not cols:
            cols = [c for c in data.columns if c != x]
        
        line = self.plot_space(t_axis_data, line=ax)
        for col in cols:
            print(col)
            line = self._add_line(line, data[col], col)
        return line

    def set_title(self, title: str):
        self.title = title
    
    def lineplot(self, data: pd.DataFrame = None, x="dt", *, y=None, show=False):
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
                    start_value=0,
                    end_value=100,
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
                feature=ToolBoxFeatureOpts(
                    data_zoom=ToolBoxFeatureDataZoomOpts(zoom_title="Zoom",
                                                         back_title="Undo Zoom"),
                    restore=ToolBoxFeatureRestoreOpts(title="Restore"),
                    data_view=ToolBoxFeatureDataViewOpts(title="View",
                                                         lang=["View data", 
                                                               "Back",
                                                               "Back"]
                                                         ),
                    save_as_image=ToolBoxFeatureSaveAsImageOpts(title="Download"),
                    
                    magic_type={},
                    brush={}
                    
                )
            ),
        )
        b = line
        if show:
            st_pyecharts(b)
        return b
    
    @staticmethod
    def py_show(ax) -> None:
        # TODO
        raise NotImplementedError
    
    @staticmethod
    def st_show(fig):
        if isinstance(fig, (list, tuple)):
            try:
                
                for j, col_fig in enumerate(fig):
                    try:
                        cols = st.columns(len(fig))
                        with cols[j]:
                            for row in col_fig:
                                st_pyecharts(row)
                                
                    except Exception as e:
                        for row in fig:
                            st_pyecharts(row)
                            print(e)
                            
            except Exception as e:
                print(e)
        else:
            st_pyecharts(fig)
                

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