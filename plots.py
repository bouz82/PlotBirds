#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import fsspec
import plotly.express as px
import plotly.io as pio


def plot_species(data, colors='black'):
    """plot data using geopandas"""
    
    url = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip"
    
    with fsspec.open(f"simplecache::{url}") as file:
        
        countries = gpd.read_file(file)
    
    xmin = 3
    xmax = 7.2
    ymin = 50.5
    ymax = 53.7
    
    with fsspec.open(f"simplecache::{url}") as file:
        
        countries = gpd.read_file(file)
    
    if isinstance(data, list) and not isinstance(colors, list):
        
        return "provide list of colors with list of species"
    
    if isinstance(data, pd.DataFrame):
        print(colors)
        
        fig, ax = plt.subplots(figsize=(8,6))

        countries[countries["ADMIN"] == "Netherlands"].plot(color="lightgrey", ax=ax)

        data.plot(x="lon", y="lat", kind="scatter", c=colors,
                colormap="YlOrRd", 
                ax=ax)
        
        ax.set_xlim([xmin, xmax])
        ax.set_ylim([ymin, ymax])
        ax.grid(alpha=0.5)

        plt.show()
        
    elif isinstance(data, list):
        
        fig, ax = plt.subplots(figsize=(8,6))

        countries[countries["ADMIN"] == "Netherlands"].plot(color="lightgrey", ax=ax)

        for species, color in zip(data, colors):
            print(species, color)
            
            species.plot(x="lon", y="lat", kind="scatter", c=color,
                    colormap="YlOrRd", 
                    ax=ax)
        
        
        ax.set_xlim([xmin, xmax])
        ax.set_ylim([ymin, ymax])
        ax.grid(alpha=0.5)

        plt.show()
        

def time_hist(data):
    """Histogram of species observations"""
    
    data = data[~data['time'].isna()]
    
    data['hour'] = data['time'].str.extract('(^\d{2})').astype(float)

    data.plot(y='hour', kind="hist")



def plot_species_map(data):
    """plot species on interactive Open Street Map"""
    
    pio.renderers.default='browser'
    
    if isinstance(data, pd.DataFrame):
        
        color_scale = [(0, 'black')]
        
        fig = px.scatter_mapbox(data, 
                                lat='lat', 
                                lon='lon',
                                hover_data=['date_time', 'number_behavior', 'location'],
                                color_discrete_sequence=color_scale,
                                color='species')
    
    
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()        
        
        
    if isinstance(data, dict):
          
        plot_data = pd.DataFrame()
        
        for color, species in data.items():
            
            plot_data = pd.concat([plot_data, species])
        
        color_scale = [(i, color) for i in range(0, len(data))]
        
        color_scale = list(data.keys())
      
        fig = px.scatter_mapbox(plot_data, 
                                lat='lat', 
                                lon='lon',
                                hover_data=['date_time', 'number_behavior', 'location'],
                                color_discrete_sequence=color_scale,
                                color='species')
    
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()



# data_dir = "/Users/zimbo/Documents/PythonProjects/waarneming/data/"

# kl_jager_recent = pd.read_pickle(data_dir + "kl_jager.pkl")
# zw_specht_recent = pd.read_pickle(data_dir + "zw_specht.pkl")
# gr_specht_recent = pd.read_pickle(data_dir + "gr_specht.pkl")
# kb_specht_recent = pd.read_pickle(data_dir + "kb_specht.pkl")
# kleine_jager_texel = pd.read_pickle(data_dir + "kleine_jager_texel_2020-2023.pkl")
# kl_jager_zuidpier = pd.read_pickle(data_dir + "kleine_jager_zuidpier_2020-2023.pkl")
# pa_strandloper_zuidpier = pd.read_pickle(data_dir + "paarse_strandloper_zuidpier_2020-2023.pkl")




# time_hist(kleine_jager_texel)

# # plot_species([zw_specht_recent, gr_specht_recent, kb_specht_recent],
# #              ['black', 'green', 'red'])

# plot_species(kleine_jager_texel)

# time_hist(pa_strandloper_zuidpier)

# plot_species(kl_jager_recent)
