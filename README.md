# PlotBirds
Plot bird co-occurrence based on waarneming.nl

## Manual
Plot occurrences of multiple species in the last n days:

```python
from waarneming import get_observations
from plots import plot_species_map, time_hist

zwarte_specht = 759
gr_specht = 40

zwarte_specht_data = get_observations(zwarte_specht, nr_of_days=7)
groene_specht_data = get_observations(gr_specht, nr_of_days=7)

plot_species_map({'black': zwarte_specht_data,
                  'green': groene_specht_data})
```
