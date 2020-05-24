"""Categorical plots"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

__all__ = [
    "bar_plot",
    "time_bar_plot"
]


class _CategoricalPlotter(object):
    def __init__(self,
                 data: pd.DataFrame,
                 x: str = None,
                 y: str = None,
                 figsize: tuple = None):
        """
        Plotter class.
        It can do something standard operations with data
        and generate matplotlib plots.

        Parameters
        ----------

        :param data: DataFrame, required.
            Input data.
        :param x: str, optional.
            x-axis values column name. If there is None, x-axis values are index.
        :param y: str, required.
            y-axis values column name.
        :param figsize: tuple, optional.
            Tuple (width, height) in inches.
        """
        plt.style.use(["seaborn", {"legend.frameon": True}])

        self.data = data.copy()
        self.figsize = figsize

        if isinstance(data, pd.DataFrame):
            for col in [x, y]:
                assert col is None or col in data.columns, f"Column {col} is not in data."
            self.x = x
            self.y = y
        else:
            raise ValueError(f"Parameter 'data' has wrong type: {type(data)}. "
                             f"pandas.DataFrame is needed.")

    def plot(self,
             kind: str = None,
             ax: plt.Axes = None,
             aggfunc: object = np.mean,
             logx: bool = False,
             logy: bool = False):
        """
        Usual plot with aggregated data.

        Parameters
        ----------

        :param kind: str, required.
            Kind of plot.
            See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html.
        :param ax: matplotlib.axes.Axes, optional.
            Axes to plot on, otherwise uses current axes.
        :param aggfunc: function, list of functions, dict, default numpy.mean, optional.
            If list of functions passed, the resulting pivot table will have hierarchical columns
            whose top level are the function names (inferred from the function objects themselves).
            If dict is passed, the key is column to aggregate and value is function or list of functions.
        :param logx: bool, optional.
            If true, x-axis will be logarithmic.
        :param logy:
            If true, y-axis will be logarithmic.

        Returns
        ----------
        :return: matplotlib.axes.Axes, optional.
            Axes to plot on.
        """
        if self.x is None:
            self.x = "_index"
            self.data[self.x] = self.data.index
        pivot_table = pd.pivot_table(self.data, index=self.x, values=self.y, aggfunc=aggfunc)
        pivot_table.plot(ax=ax, y=self.y, kind=kind,
                         figsize=self.figsize,
                         logx=logx, logy=logy, legend=True)
        return ax

    def grouped_plot(self,
                     kind: str = None,
                     ax: plt.Axes = None,
                     hue: str = None,
                     norm: bool = False,
                     aggfunc: object = np.mean,
                     logx: bool = False,
                     logy: bool = False):
        """
        Plot with data grouping.

        Parameters
        ----------

        :param kind: str, required.
            Kind of plot.
            See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html.
        :param ax: matplotlib.axes.Axes, optional.
            Axes to plot on, otherwise uses current axes.
        :param hue: str, optional.
            Grouped column name.
        :param norm: bool, optional.
            If true, every bar will be normalized.
        :param aggfunc: function, list of functions, dict, default numpy.mean, optional.
            If list of functions passed, the resulting pivot table will have hierarchical columns
            whose top level are the function names (inferred from the function objects themselves).
            If dict is passed, the key is column to aggregate and value is function or list of functions.
        :param logx: bool, optional.
            If true, x-axis will be logarithmic.
        :param logy:
            If true, y-axis will be logarithmic.

        Returns
        ----------
        :return: matplotlib.axes.Axes, optional.
            Axes to plot on.
        """
        if self.x is None:
            self.x = "_index"
            self.data[self.x] = self.data.index
        self.data.set_index(hue, drop=True, inplace=True)

        pivot_table = self.data.pivot_table(index=self.x, columns=hue, values=self.y,
                                            aggfunc=aggfunc)
        if norm:
            pivot_table = pivot_table.divide(pivot_table.sum(axis=1), axis=0)

        pivot_table.plot(ax=ax, stacked=True, kind=kind,
                         figsize=self.figsize,
                         logx=logx, logy=logy, legend=True)

        if norm:
            plt.legend(bbox_to_anchor=(1, 1))
        else:
            plt.legend(loc="best")
        return ax

    def calculate_pretty_ticks(self, ticks, axissize):
        if len(ticks[0]) > axissize:
            step_size = int(len(ticks[0]) // axissize)
        else:
            step_size = 1
        return ticks[0][::-step_size][::-1], ticks[1][::-step_size][::-1]


def bar_plot(data=None, x=None, y=None, hue=None, norm=False,
             ax=None, figsize=None, orient="v", aggfunc=np.mean,
             logx=False, logy=False):
    """
    Simple bar plot.

    Parameters
    ----------

    :param data: DataFrame, required.
        Input data.
    :param x: str, optional.
        x-axis values column name. If there is None, x-axis values are index.
    :param y: str, required.
        y-axis values column name.
    :param hue: str, optional.
        Grouped column name.
    :param norm: bool, optional.
        If true, every bar will be normalized.
    :param ax: matplotlib.axes.Axes, optional.
        Axes to plot on, otherwise uses current axes.
    :param figsize: tuple, optional.
        Tuple (width, height) in inches.
    :param orient: str, optional.
        Orient of plot. Can equal "v" or "h".
    :param aggfunc: function, list of functions, dict, default numpy.mean, optional.
        If list of functions passed, the resulting pivot table will have hierarchical columns
        whose top level are the function names (inferred from the function objects themselves).
        If dict is passed, the key is column to aggregate and value is function or list of functions.
    :param logx: bool, optional.
        If true, x-axis will be logarithmic.
    :param logy:
        If true, y-axis will be logarithmic.

    Returns
    ----------
    :return: matplotlib.axes.Axes, optional.
        Axes to plot on.
    """
    plotter = _CategoricalPlotter(data, x, y, figsize)

    if ax is None:
        ax = plt.gca()

    if hue is None:
        plotter.plot(kind="bar" if orient == "v" else "barh",
                     ax=ax, aggfunc=aggfunc, logx=logx, logy=logy)
    else:
        plotter.grouped_plot(kind="bar" if orient == "v" else "barh",
                             ax=ax, hue=hue, norm=norm, logx=logx, logy=logy)
    return ax


def time_bar_plot(data=None, x=None, y=None, hue=None, period=None,
                  norm=False, ax=None, figsize=None, xlabelformat="%d-%m",
                  aggfunc=np.mean, logx=False, logy=False):
    """
    Bar plot with time x-axis.

    Parameters
    ----------

    :param data: DataFrame, required.
        Input data.
    :param x: str, optional.
        x-axis values column name. If there is None, x-axis values are index.
    :param y: str, required.
        y-axis values column name.
    :param hue: str, optional.
        Grouped column name.
    :param period: str or pandas.Offset, required.
        One of pandas’ offset strings or an Offset object.
        See https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases.
    :param norm: bool, optional.
        If true, every bar will be normalized.
    :param ax: matplotlib.axes.Axes, optional.
        Axes to plot on, otherwise uses current axes.
    :param figsize: tuple, optional.
        Tuple (width, height) in inches.
    :param xlabelformat: str, optional.
        Explicit format string.
        See https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior.
    :param aggfunc: function, list of functions, dict, default numpy.mean, optional.
        If list of functions passed, the resulting pivot table will have hierarchical columns
        whose top level are the function names (inferred from the function objects themselves).
        If dict is passed, the key is column to aggregate and value is function or list of functions.
    :param logx: bool, optional.
        If true, x-axis will be logarithmic.
    :param logy:
        If true, y-axis will be logarithmic.

    Returns
    ----------
    :return: matplotlib.axes.Axes, optional.
        Axes to plot on.
    """
    data = data.copy()
    if x is None:
        x = "_index"
        data[x] = pd.to_datetime(data.index).tz_localize(None) \
                    .to_period(period) \
                    .start_time
    else:
        data[x] = pd.to_datetime(data[x]).tz_localize(None) \
                    .to_period(period) \
                    .start_time
    plotter = _CategoricalPlotter(data, x, y, figsize)

    if ax is None:
        ax = plt.gca()

    if hue is None:
        plotter.plot(kind="bar",
                     ax=ax, aggfunc=aggfunc, logx=logx, logy=logy)
    else:
        plotter.grouped_plot(kind="bar",
                             ax=ax, hue=hue, norm=norm, logx=logx, logy=logy)

    ticks, labels = plotter.calculate_pretty_ticks(plt.xticks(), plt.rcParams.get('figure.figsize')[0])
    ax.set_xticks(ticks)
    ax.set_xticklabels(map(lambda period: pd.Timestamp(period.get_text()).strftime(xlabelformat),
                           labels), rotation=0 if "y" not in xlabelformat.lower() else 45)
    ax.set_xlabel("time")
    return ax
