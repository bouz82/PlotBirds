# PlotBirds
Plot bird co-occurrence based on waarneming.nl

## Manual
Species and location ID's can be found in the waarneming url's:
https://waarneming.nl/locations/**9114**/observations/?date_after=2022-11-03&date_before=2023-11-03&species=**759**
https://waarneming.nl/species/**759**/observations/?


```python
from waarneming import get_observations
from plots import plot_species_map, time_hist

# Plot occurrences of multiple species in the last n days:
zwarte_specht = 759
gr_specht = 40

zwarte_specht_data = get_observations(zwarte_specht, nr_of_days=7)
groene_specht_data = get_observations(gr_specht, nr_of_days=7)

plot_species_map({'black': zwarte_specht_data,
                  'green': groene_specht_data})

# Plot occurrences of multiple species in a specific date range:
zwarte_specht_data = get_observations(zwarte_specht, date_after='2022-11-03', date_before='2022-11-05')
groene_specht_data = get_observations(gr_specht, date_after='2022-11-03', date_before='2022-11-05')

plot_species_map({'black': zwarte_specht_data,
                  'green': groene_specht_data})


# Limit observations to specific location:
rotgans = 172
texel = 22650

rotgans_data = get_observations(rotgans, location=texel, date_after='2023-11-03', date_before='2023-11-03')

plot_species_map({'black': rotgans_data})
```
