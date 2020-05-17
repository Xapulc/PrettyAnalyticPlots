import pandas as pd
import matplotlib.pyplot as plt

__all__ = [
    "bar_plot"
]


class _CategoricalPlotter(object):
    def __init__(self,
                 data: pd.DataFrame,
                 x: str = None,
                 y: str = None,
                 hue: str = None,
                 x_label: str = None,
                 y_label: str = None,
                 hue_label: str = None,
                 figsize: tuple = None,
                 title: str = None):
        plt.style.use('seaborn')

        self.data = data
        self.x_label = x_label if x_label is not None else x
        self.y_label = y_label if y_label is not None else y
        self.hue_label = hue_label if hue_label is not None else hue
        self.figsize = figsize
        self.title = title

        if isinstance(data, pd.DataFrame):
            for col in [x, y, hue]:
                assert col is None or col in data.columns, f"Column {col} is not in data."
            self.x = x
            self.y = y
            self.hue = hue
        else:
            raise ValueError(f"Parameter 'data' has wrong type: {type(data)}. "
                             f"pandas.DataFrame is needed.")

    def bar_plot(self,
                 ax: plt.Axes = None,
                 orient="v",
                 logx=False,
                 logy=False):
        if self.hue is not None:
            if self.x is None:
                self.x = "_index"
                self.data[self.x] = self.data.index
            self.data.set_index(self.hue, drop=True, inplace=True)

            pivot_table = self.data.pivot_table(index=self.x, columns=self.hue, values=self.y, aggfunc="sum")
            pivot_table.plot(ax=ax, stacked=True,
                             kind="bar" if orient == "v" else "barh",
                             title=self.title, figsize=self.figsize,
                             logx=logx, logy=logy, legend=True)

        else:
            self.data.plot(ax=ax, x=self.x, y=self.y,
                           kind="bar" if orient == "v" else "barh",
                           title=self.title, figsize=self.figsize,
                           logx=logx, logy=logy, legend=True)

        ax.set_xlabel(self.x_label)
        ax.set_ylabel(self.y_label)
        return ax


def bar_plot(data=None,
             x=None,
             y=None,
             hue=None,
             ax=None,
             x_label=None,
             y_label=None,
             hue_label=None,
             fig_shape=None,
             title=None,
             orient="v",
             logx=False,
             logy=False,
             ):
    plotter = _CategoricalPlotter(data, x, y, hue, x_label, y_label, hue_label,
                                  fig_shape, title)

    if ax is None:
        ax = plt.gca()

    plotter.bar_plot(ax, orient, logx, logy)
    return ax
