## Visualization

1. Heatmap Chart
2. Bubble Chart
3. Statistic Chart

## Commands

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report

# Run it in public in GCP.
HOST='0.0.0.0' PORT=8080 npm start
```


## Datasets (total size: ~350 GB)

### 1. Commuters

- MTA: [2014-2015 MTA turnstile data in New York City ](http://web.mta.info/developers/turnstile.html) (900MB)
       [New York City MTA Station Location](http://web.mta.info/developers/data/nyct/subway/Stations.csv)
- Taxis: [2014 Yellow Taxi Trip Data](https://data.cityofnewyork.us/Transportation/2014-Yellow-Taxi-Trip-Data/gn7m-em8n) (25GB)

### 2. Crimes

- Crime: [2014-2015 Crimes reported in all 5 boroughs of New York City](https://www.kaggle.com/adamschroeder/crimes-new-york-city#Crime_Column_Description.csv)

### 3. Sentiment

- Download and extract from really large archive dataset (all month twitter information). (https://archive.org/details/twitterstream?and[]=year%3A%222014%22)

  - 2014-02: https://archive.org/details/archiveteam-twitter-stream-2014-02 (33.8GB)
  - 2014-03: https://archive.org/details/archiveteam-twitter-stream-2014-03 (46.2GB)
  - 2014-04: https://archive.org/details/archiveteam-twitter-stream-2014-04 (45.1GB)
  - 2014-05: https://archive.org/details/archiveteam-twitter-stream-2014-05 (44.7GB)
  - 2014-10: https://archive.org/details/archiveteam-twitter-stream-2014-10 (47.6GB)
  - 2014-11: https://archive.org/details/archiveteam-twitter-stream-2014-11 (47.5GB)
  - 2014-12: https://archive.org/details/archiveteam-twitter-stream-2014-12 (48.8GB)
 
- Process the data and extract twitter in New York and tweet time.


### 4. Number of residents (1MB)

Population / Age / Sex: Decennial Census - Census 2010 - https://www1.nyc.gov/site/planning/data-maps/nyc-population/census-2010.page

> Similar as what has done in this website: https://popfactfinder.planning.nyc.gov/?lastreport=census#12.79/40.77387/-73.95082
> 
> Decennial Census
> Every ten years the U. S. Census Bureau conducts a decennial census, primarily for purposes of congressional reapportionment. These censuses count every person in the country and collect only the most basic demographic and housing characteristics (like, age, sex, race, and housing tenure). The decennial census provides the most accurate and detailed understanding about the count and distribution of the U. S. population. It is also important to note that private information (such as names and addresses) collected through the census is protected under Title 13 of U. S. Code. To ensure census participant confidentiality, data are never published below the block-level. Consequently, census blocks are the smallest geography used in New York City Population FactFinder (PFF). Beyond census blocks, PFF also re-publishes decennial census data from 2000 and 2010 at the census tract-, Neighborhood Tabulation Area-, and Public Use Microdata Area-levels.

### 5. Geographic of Manhattan (precinct map)

According [wiki](https://en.wikipedia.org/wiki/List_of_Manhattan_neighborhoods) the following approximate definitions are used:

Upper Manhattan is the area above 96th Street.
Uptown Manhattan is the area above 59th Street;
Midtown Manhattan is the area between 34th Street and 59th Street.
Downtown Manhattan is the area below 14th Street; 
Lower Manhattan is the area below Chambers Street. (We didn't sperate Downtown and Lower Manhattan)

- Downtown: https://www.google.com/maps/place/Lower+Manhattan,+New+York,+NY/@40.7215259,-74.0129994,14z/data=!3m1!4b1!4m5!3m4!1s0x89c259885419838b:0x2d39c2f6ed6db3c!8m2!3d40.7218345!4d-73.9998354

- Midtown: https://www.google.com/maps/place/Midtown,+New+York,+NY/@40.7505189,-74.0014333,14z/data=!3m1!4b1!4m5!3m4!1s0x89c25901a4127ca9:0xbecdcc9081d6cfdb!8m2!3d40.7549309!4d-73.9840195

- Uptown and Uppertown (same in google, but different in [wiki](https://en.wikipedia.org/wiki/List_of_Manhattan_neighborhoods), we use the way to seperate uptown and uppertown in wiki.): https://www.google.com/maps/place/Upper+Manhattan,+New+York,+NY/@40.8305616,-73.9759374,13z/data=!3m1!4b1!4m5!3m4!1s0x89c2f6131f319d63:0x158166d40c6168ed!8m2!3d40.8240478!4d-73.9447643

![Manhattan_neighborhoods](https://upload.wikimedia.org/wikipedia/commons/5/5a/Manhattan_neighborhoods.png)
