import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

__all__ = [
    "bar_plot"
]


class _CategoricalPlotter(object):
    def __init__(self,
                 data: pd.DataFrame,
                 x: str = None,
                 y: str = None,
                 figsize: tuple = None):
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


def bar_plot(data=None, x=None, y=None, hue=None, norm=False,
             ax=None, figsize=None, orient="v", aggfunc=np.mean,
             logx=False, logy=False):
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
