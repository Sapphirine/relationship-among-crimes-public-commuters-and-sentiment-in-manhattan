## Visualization

1. Heatmap Chart
2. Bubble Chart
3. Statistic Chart

## Reports

> folder: _reports/

### Project Proposal: [PDF](https://github.com/zhichengMLE/relationship-among-crimes-public-commuters-and-sentiment-in-manhattan/blob/master/_reports/BigData_ProjectProposal.pdf) [PPT](https://github.com/zhichengMLE/relationship-among-crimes-public-commuters-and-sentiment-in-manhattan/blob/master/_reports/BigData_ProjectProposal.pptx) [Youtube](https://youtu.be/vOyisfkSr_E)


### Final Presentation: [PDF](https://github.com/zhichengMLE/relationship-among-crimes-public-commuters-and-sentiment-in-manhattan/blob/master/_reports/BigData_FinalPresentation.pdf) [PPT](https://github.com/zhichengMLE/relationship-among-crimes-public-commuters-and-sentiment-in-manhattan/blob/master/_reports/BigData_FinalPresentation.pptx) [Youtube](https://youtu.be/UyrvJuL0Wn4) [Report](https://github.com/zhichengMLE/relationship-among-crimes-public-commuters-and-sentiment-in-manhattan/blob/master/_reports/Relationship_among_Crimes_Public_Commuters_and_Sentiment_in_Manhattan.pdf)



## Commands

``` bash
# Clone repository
git clone git@github.com:zhichengMLE/relationship-among-crimes-public-commuters-and-sentiment-in-manhattan.git

# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# Run it in public in GCP.
HOST='0.0.0.0' PORT=8080 npm start

```


## Diagrams

### System Diagram

![system_diagram](https://raw.githubusercontent.com/zhichengMLE/relationship-among-crimes-public-commuters-and-sentiment-in-manhattan/master/static/images/system_diagram.png)


### Data Processing

![data_processing](https://raw.githubusercontent.com/zhichengMLE/relationship-among-crimes-public-commuters-and-sentiment-in-manhattan/master/static/images/data_processing.png)

### Data Visualization


![data_visualization](https://raw.githubusercontent.com/zhichengMLE/relationship-among-crimes-public-commuters-and-sentiment-in-manhattan/master/static/images/data_visualization.png)

## Datasets (total size: ~339.6 GB)

### 1. Crimes (53MB)

- Crime: [2014-2015 Crimes reported in all 5 boroughs of New York City](https://www.kaggle.com/adamschroeder/crimes-new-york-city#Crime_Column_Description.csv) (53MB)

### 2. Public Commuters (25.9GB)

- MTA (subway): 

   - [2014-2015 MTA turnstile data in New York City ](http://web.mta.info/developers/turnstile.html) (900MB)
        
   - [New York City MTA Station Location](http://web.mta.info/developers/data/nyct/subway/Stations.csv) (very small)
       
- Taxis: [NYC 2014 Yellow Taxi Trip Data](https://data.cityofnewyork.us/Transportation/2014-Yellow-Taxi-Trip-Data/gn7m-em8n) (25GB)


### 3. Sentiment (313.7GB)

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

## Algorithms, Packages, and Tools

### The algorithms that we had used are listed below.

- Natural Language Processing. We use NLP-based algorithm to process twitter dataset to get sentiment value. We use TextBlob which is a Python package of using \textit{NLTK} and pattern to process context.

- Calculate Point inside/outside of Polygon. We use this algorithm to convert coordinate to precinct number.

- Calculate Geo Center of Polygon. We use this algorithm to put the precinct number of the map which provide better visualization effect.
    
- Linear Regression. We use linear regression to fit the model in bubble chart which help to explore the linear relationship of number of crime and number of commuters.
    
- Correlation Algorithms. We use three different correlation algorithm (\ie, Pearson, Kendall, and Spearman) in statistic to better evaluate the correlation of data.


### The packages and tools that we had utilized are summarized below.



- Google Cloud Platform. In order to process really large amount of dataset, we use this to store and process data.

- Pandas. We use this package to process large amount of data chunk by chuck in relatively fast speed.

- Numpy. We use Numpy to boost the speed of matrix computation.
    
- Shapely. Shapely is a Python package for manipulation and analysis of planar geometric objects. We use it to calculate coordinate point inside/outside precinct polygon.
    
- {TextBlob. TextBlob is a Python package of using \textit{NLTK} and pattern to process context. We use it to process Twitter context and calculate sentiment polarity.
    
- Vue.js. We use Vue.js to design the website because it supports the definition of component which could be reused in different pages.
    
- D3.js. We use powerful function of D3.js to manipulate DOM in HTML based on data. Also, the official site of D3.js provides great example which helps us get started.














## Web UIs

### Homepage

![heatmap_chart](https://raw.githubusercontent.com/zhichengMLE/relationship-among-crimes-public-commuters-and-sentiment-in-manhattan/master/static/images/homepage.png)

### Heatmap Chart

![heatmap_chart](https://raw.githubusercontent.com/zhichengMLE/relationship-among-crimes-public-commuters-and-sentiment-in-manhattan/master/static/images/heatmap_chart.png)

### Bubble Chart

![heatmap_chart](https://raw.githubusercontent.com/zhichengMLE/relationship-among-crimes-public-commuters-and-sentiment-in-manhattan/master/static/images/bubble_chart.png)

### Statistic Chart


![heatmap_chart](https://raw.githubusercontent.com/zhichengMLE/relationship-among-crimes-public-commuters-and-sentiment-in-manhattan/master/static/images/statistic_chart.png)


## Experiment Results

- From the heatmap charts, we can see that there are more commuters and crimes in downtown and midtown, while less in the uptown and upper town.

- From the Pearson correlation calculated, we can see that the number of crimes and commuters are basically positive correlated (about 0.5).

- From the sentiment analysis, we can see that for the weekdays, people normally more negative during the work hours and they tend to feel more positive after work. While for the weekend, people would be more positive all the day which may result in safety awareness decreasing and lead number of crimes increase.

- There are also some special events during in people's life. The Wednesday is the saddest day during the whole week, especially during the day time. There is very limited commute while crimes drop a little. People have the most negative mood. The weekend, including the Friday night, has the most high positive feelings.
- During this time, crimes increase sharply while the city has a high commute population.


## Conclusion

From the heat map charts, we notice that there are more commuters and crimes in downtown and midtown, while less in the uptown and upper town. From the Pearson correlation calculated, we can see that the number of crimes and com- muters are basically positive correlated (about 0.5). From the sentiment analysis, we found that for the weekdays, people are more negative during work hours and they tend to feel more positive after work. But for the weekend, people would be more positive all the day which may result in safety awareness decreasing and lead number of crimes increase. There are also some special events during in people’s life. The Wednesday is the saddest day during the whole week, especially during the daytime. There is very limited commute while crimes drop a little. People have the most negative mood. The weekend, including the Friday night, has the highest positive feelings. During this time, crimes increase sharply while the city has a high commuter population. We can make the conclusion that, the crimes have a tight relationship between the city commute population and people sentiment polarity. When the commute population increase, the number of crimes increase. When the sentiment is more positive, the more crimes happen.
