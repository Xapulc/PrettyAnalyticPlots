# Pretty Analytic Plots

This project simplifies the construction of charts
typical of an analyst.

## Installing

Install package:
```
python3 project_path/setup.py install
```
Dependencies will be installed along with the package.

### Some pretty plots

If you want to plot normalized bar plot, 
you can write
```
from seaborn import load_dataset
flights = load_dataset("flights", index_col=False)
bar_plot(flights, ax=ax, x="year", y="passengers", hue="month", norm=True)
```
![Plot](examples/img.png)

You can find more usage examples in [examples](examples).

## Built With

* [Seaborn](https://seaborn.pydata.org/) - Main mastermind
* [Matplotlib](https://matplotlib.org/) - Visualization library
* [Pandas](https://pandas.pydata.org/) - Data Analysis library

## Authors

* **Victor Kharlamov** - *Developer* - [Xapulc](https://github.com/Xapulc)

See also the list of 
[contributors](https://github.com/Xapulc/PrettyAnalyticPlots/contributors) 
who participated in this project.

## License

This project is licensed under the BSD License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to [seaborn](https://github.com/mwaskom/seaborn)
for architectural solutions used in this project.
