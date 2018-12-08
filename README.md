## Main Steps

1. Map Plot (Heatmap)
2. Chart Plot
3. Statistic Plot

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


## Datasets (total size: XX GB)

### 1. Commuters

- MTA
- Taxis

### 2. Crimes

- Crime: https://www.kaggle.com/adamschroeder/crimes-new-york-city#Crime_Column_Description.csv

### 3. Sentiment

- Ask for dataset via paper: http://www.cs.columbia.edu/~julia/papers/Agarwaletal11.pdf

### 4. Number of residents

- Aggregate # of residents via this website: https://popfactfinder.planning.nyc.gov/?lastreport=census#12.79/40.77387/-73.95082

### 5. Geographic of Manhattan (precinct map)

- Downtown: https://www.google.com/maps/place/Lower+Manhattan,+New+York,+NY/@40.7215259,-74.0129994,14z/data=!3m1!4b1!4m5!3m4!1s0x89c259885419838b:0x2d39c2f6ed6db3c!8m2!3d40.7218345!4d-73.9998354

- Midtown: https://www.google.com/maps/place/Midtown,+New+York,+NY/@40.7505189,-74.0014333,14z/data=!3m1!4b1!4m5!3m4!1s0x89c25901a4127ca9:0xbecdcc9081d6cfdb!8m2!3d40.7549309!4d-73.9840195

- Uptown and Uppertown (same in google, but different in wiki (https://en.wikipedia.org/wiki/List_of_Manhattan_neighborhoods), we use the way to seperate uptown and uppertown in wiki.): https://www.google.com/maps/place/Upper+Manhattan,+New+York,+NY/@40.8305616,-73.9759374,13z/data=!3m1!4b1!4m5!3m4!1s0x89c2f6131f319d63:0x158166d40c6168ed!8m2!3d40.8240478!4d-73.9447643



