import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .plotter import _Plotter

__all__ = [
    "bar_plot",
    "time_bar_plot",
    "line_plot",
    "time_line_plot"
]


def bar_plot(data, y, x=None, hue=None, norm=False,
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
    :param logy: bool, optional
        If true, y-axis will be logarithmic.

    Returns
    ----------
    :return: matplotlib.axes.Axes, optional.
        Axes to plot on.
    """
    plotter = _Plotter(data, x, y, figsize)

    if ax is None:
        ax = plt.gca()

    kind = "bar" if orient == "v" else "barh"
    if hue is None:
        plotter.plot(kind=kind, ax=ax, aggfunc=aggfunc, logx=logx, logy=logy)
    else:
        plotter.grouped_plot(kind=kind, stacked=True,
                             ax=ax, hue=hue, norm=norm, logx=logx, logy=logy)
    return ax


def time_bar_plot(data, y, x=None, hue=None, period=None,
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
    :param logy: bool, optional.
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
    plotter = _Plotter(data, x, y, figsize)

    if ax is None:
        ax = plt.gca()

    if hue is None:
        plotter.plot(kind="bar",
                     ax=ax, aggfunc=aggfunc, logx=logx, logy=logy)
    else:
        plotter.grouped_plot(kind="bar", stacked=True,
                             ax=ax, hue=hue, norm=norm, logx=logx, logy=logy)

    ticks, labels = plotter.calculate_pretty_ticks(plt.xticks(), plt.rcParams.get('figure.figsize')[0])
    ax.set_xticks(ticks)
    ax.set_xticklabels(map(lambda period: pd.Timestamp(period.get_text()).strftime(xlabelformat), labels),
                       rotation=0 if "y" not in xlabelformat.lower() else 45)
    ax.set_xlabel("time")
    return ax


def line_plot(data, y, x=None, hue=None, norm=False,
              stacked=False, ax=None, figsize=None, aggfunc=np.mean,
              logx=False, logy=False):
    """
    Simple line plot.

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
    :param stacked: bool, optional.
        If true, create stacked plot.
    :param ax: matplotlib.axes.Axes, optional.
        Axes to plot on, otherwise uses current axes.
    :param figsize: tuple, optional.
        Tuple (width, height) in inches.
    :param aggfunc: function, list of functions, dict, default numpy.mean, optional.
        If list of functions passed, the resulting pivot table will have hierarchical columns
        whose top level are the function names (inferred from the function objects themselves).
        If dict is passed, the key is column to aggregate and value is function or list of functions.
    :param logx: bool, optional.
        If true, x-axis will be logarithmic.
    :param logy: bool, oprional.
        If true, y-axis will be logarithmic.

    Returns
    ----------
    :return: matplotlib.axes.Axes, optional.
        Axes to plot on.
    """
    plotter = _Plotter(data, x, y, figsize)

    if ax is None:
        ax = plt.gca()

    if hue is None:
        plotter.plot(kind="line", ax=ax, aggfunc=aggfunc, logx=logx, logy=logy)
    else:
        plotter.grouped_plot(kind="line", stacked=stacked,
                             ax=ax, hue=hue, norm=norm, logx=logx, logy=logy)
    return ax


def time_line_plot(data, y, x=None, hue=None, period=None, stacked=False,
                   norm=False, ax=None, figsize=None, xlabelformat="%d-%m",
                   aggfunc=np.mean, logx=False, logy=False):
    """
    Line plot with time x-axis.

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
    :param stacked: bool, optional.
        If true, create stacked plot.
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
    :param logy: bool, optional.
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
    plotter = _Plotter(data, x, y, figsize)

    if ax is None:
        ax = plt.gca()

    if hue is None:
        plotter.plot(kind="line",
                     ax=ax, aggfunc=aggfunc, logx=logx, logy=logy)
    else:
        plotter.grouped_plot(kind="line", stacked=stacked,
                             ax=ax, hue=hue, norm=norm, logx=logx, logy=logy)

    ticks, labels = plotter.calculate_pretty_ticks(plt.xticks(), plt.rcParams.get('figure.figsize')[0])
    ax.set_xticks(ticks)
    ax.set_xticklabels(map(lambda period: pd.Timestamp(period.get_text()).strftime(xlabelformat), labels),
                       rotation=0 if "y" not in xlabelformat.lower() else 45)
    ax.set_xlabel("time")
    return ax
