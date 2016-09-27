# Prediction of Zika Outbreaks

by Michelle L. Gill, Ph.D.  

## Summary

This is my third project for the Summer 2016 [Metis Data Science Bootcamp](http://thisismetis.com), which incorporated supervised machine learning, PostgreSQL, and D3 for visualization. For this project, whether or not a region would would have an outbreak of Zika virus.

## Blog Post

A blog post on [themodernscientist](http://themodernscientist.com) will be available the week of 2016/09/26. This text will be updated when the website is posted.

## Repo Contents

* **environment.yml**: list of conda python libraries that were used during analysis
* **figures**: images used on the presentation
* **map**: D3 animated timeline used during presentation. A [movie](https://mlgill.github.io/zika_prediction/figures/d3_visualization.mp4) of the animation is also available
* **notebooks**: Jupyter notebooks used for analysis
* **presentation**: [PDF](https://github.com/mlgill/zika_prediction/blob/master/presentation/Predicting_Zika_Outbreaks.pdf) 

## Data Sources

This project made extensive use of external data sources, including data from GitHub repos and that was scraped from various websites.

1. Zika outbreak data was pulled from the CDC Epidemic Prediction Initiative [GitHub repo](https://github.com/cdcepi/zika). My project used data that was pulled on 07/30/2016, which corresponds to commit `d44c5d1ca3af633224c8b8b490b1a3aafa9bcc8e`. A clone of this commit is available [here](https://github.com/mlgill/zika).
2. Latitude and longitude data for Zika outbreaks was pulled from the following: Google Maps API, Scraped from Google Search via four proxies, and scraped from [LatLong](http://www.latlong.net/).
3. Airport location information was scraped from [Falling Rain](http://fallingrain.com).
4. Airport flight schedules were scraped from [FlightRadar24](https://www.flightradar24.com).
5. Worldwide historical weather data was scraped from [Wunderground](https://www.wunderground.com) using closest airport code as the key.
6. *Aedes aegypti* and *Aedes albopictus* occurrences were from [Dryad](http://dx.doi.org/10.5061/dryad.47v3c/1). See references below for manuscripts related to this data.
7. Worldwide population density was from the [NASA Socioeconomic Data and Applications Center (SEDAC)](http://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-density) Gridded Population and Population Density of the World.
8. World GDP and purchase parity adjusted GDP from 2015 were scraped from [Knoema](http://knoema.com).
9. Flight patterns were scraped from [FlightRadar24](http://flightradar24.com), however this data was not incorporated into the model due to time limitations. 


*References for Aedes aegypti and Aedes albopictus occurrences*

> Kraemer MUG, Sinka ME, Duda KA, Mylne A, Shearer FM, Brady OJ, Messina JP, Barker CM, Moore CG, Carvalho RG, Coelho GE, Van Bortel W, Hendrickx G, Schaffner F, Wint GRW, Elyazar IRF, Teng H, Hay SI (2015) The global compendium of Aedes aegypti and Ae. albopictus occurrence. Scientific Data 2(7): 150035. [http://dx.doi.org/10.1038/sdata.2015.35](http://dx.doi.org/10.1038/sdata.2015.35)

> Kraemer MUG, Sinka ME, Duda KA, Mylne A, Shearer FM, Brady OJ, Messina JP, Barker CM, Moore CG, Carvalho RG, Coelho GE, Van Bortel W, Hendrickx G, Schaffner F, Wint GRW, Elyazar IRF, Teng H, Hay SI (2015) Data from: The global compendium of Aedes aegypti and Ae. albopictus occurrence. Dryad Digital Repository. [http://dx.doi.org/10.5061/dryad.47v3c](http://dx.doi.org/10.5061/dryad.47v3c)
