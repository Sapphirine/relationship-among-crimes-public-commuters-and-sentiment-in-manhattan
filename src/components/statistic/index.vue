<template>
  <div class="statisticPlot">
    <h1 style="position:absolute; top:3px; left:45%; color:white">{{title}}</h1>

    <div class="container-fluid">
      <div class="statisticInfoHolder" style="margin-left: 15px;margin-right: 4px;" >
        <div class="row">
          <div class="col-sm-6 " >
            <div class="mapHolder cliente">
              <ManhattanPrecinctMap
                @precinctSelected="onPrecinctSelected"
                @precinctDeselected="onPrecinctDeselected"
                @mapIsReady="onMapIsReady"
              />
            </div>
            <div class="tooltipHolder">
              <Tooltip
                v-if="currPrecinct"
                :title="currentPrecinctTitle"
              />
            </div>
          </div>
          <div class="col-sm-3">
            <div class="card cliente">
              <div id="title">
                <h4>Crime Trend</h4>
              </div>
              <canvas id="crimeLineCanvas"></canvas>
              <div id="crimeDataText">
                <div id="dataContainer">
                  <div style="text-align:left">Current number of crime:<span style="float:right">{{curr_crime}}</span></div>
                  
                  <div style="text-align:left">Min number of crime:<span style="float:right">{{min_crime}}</span></div>

                  <div style="text-align:left">Max number of crime:<span style="float:right">{{max_crime}}</span></div>
                  
                  <div style="text-align:left">Time of min number of crime:<span style="float:right">{{min_crime_time}} h</span></div>
                  
                  <div style="text-align:left">Time of max number of crime:<span style="float:right">{{max_crime_time}} h</span></div>
                  
                  <div style="text-align:left">Ratio of Max to Min:<span style="float:right">{{max_crime_change}}</span></div>
                </div>
              </div>
            </div>

            <div class="my-3">
            </div>
            <div class="card cliente">
              <div id="title">
                <h4>Commuter Trend</h4>
              </div>
              <canvas id="trafficLineCanvas"></canvas>
              <div id="crimeDataText">
                <div id="dataContainer">
                  <div style="text-align:left">Current number of commuters:<span style="float:right">{{curr_traffic}}</span></div>
                  
                  <div style="text-align:left">Min number of commuters:<span style="float:right">{{min_traffic}}</span></div>

                  <div style="text-align:left">Max number of commuters:<span style="float:right">{{max_traffic}}</span></div>
                  
                  <div style="text-align:left">Time of min number of commuters:<span style="float:right">{{min_traffic_time}} h</span></div>
                  
                  <div style="text-align:left">Time of max number of commuters:<span style="float:right">{{max_traffic_time}} h</span></div>
                  
                  <div style="text-align:left">Ratio of Max to Min:<span style="float:right">{{max_traffic_change}}</span></div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-sm-3">
            <div class="card cliente">
              <div id="title">
                <h4>Positive Sentiment Trend</h4>
              </div>
              <canvas id="sentimentLineCanvas"></canvas>
              <div id="sentimentPosDataText">
                <div id="dataContainer">
                  <div style="text-align:left">Current sentiment ratio:<span style="float:right">{{curr_positive}}</span></div>
                  
                  <div style="text-align:left">Min sentiment ratio:<span style="float:right">{{min_positive}}</span></div>

                  <div style="text-align:left">Max sentiment ratio:<span style="float:right">{{max_positive}}</span></div>
                  
                  <div style="text-align:left">Time of min sentiment ratio:<span style="float:right">{{min_positive_time}} h</span></div>
                  
                  <div style="text-align:left">Time of max sentiment ratio:<span style="float:right">{{max_positive_time}} h</span></div>
                  
                  <div style="text-align:left">Ratio of Max to Min:<span style="float:right">{{max_positive_change}}</span></div>
                </div>
              </div>
            </div>
            <div class="my-3">
            </div>
            <div class="card cliente">
              <div id="title">
                <h4>Correlation Trend</h4>
              </div>
              <canvas id="correlationLineCanvas"></canvas>
              <div id="correlationDataText">
                <div id="dataContainer">
                  <div style="text-align:left">Min pearson correlation:<span style="float:right">{{min_pearson}} ({{min_pearson_time}} h)</span></div>

                  <div style="text-align:left">Max pearson correlation:<span style="float:right">{{max_pearson}} ({{max_pearson_time}} h)</span></div>
                  
                  <div style="text-align:left">Min kendall correlation:<span style="float:right">{{min_kendall}} ({{min_kendall_time}} h)</span></div>
                  
                  <div style="text-align:left">Max kendall correlation:<span style="float:right">{{max_kendall}} ({{max_kendall_time}} h)</span></div>
                  
                  <div style="text-align:left">Min spearman correlation:<span style="float:right">{{min_spearman}} ({{min_spearman_time}} h)</span></div>

                  <div style="text-align:left">Max spearman correlation:<span style="float:right">{{max_spearman}} ({{max_spearman_time}} h)</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
        
      <div class="sliderHolder my-3 cliente" style="margin-left: 15px;margin-right: 4px; padding-top:3px; padding-bottom:1px;">
        <div class="row">
          <div class="col-md-1">
              <div  style="float:right"><h4><span class="badge badge-pill badge-primary">Time </span> </h4></div>
              <div  style="float:right"><h4> <span class="badge badge-pill badge-primary">Day </span> </h4></div>
          </div>
          <div class="col-md-10">
            <div class="row">
              <div class="col-md-12 ml-auto mr-auto"  style="padding-left:0px; padding-right:0px">
                <vue-slider 
                  ref="hourSlider"
                  v-model="hourSliderValue"
                  v-bind="hourSliderOption"
                >
                </vue-slider>
              </div>
            </div>
            <div class="row">
              <div class="col-md-12 ml-auto mr-auto"  style="padding-left:0px; padding-right:0px">
                <vue-slider 
                  ref="daySlider"
                  v-model="daySliderValue"
                  v-bind="daySliderOption"
                >
                </vue-slider>
              </div>
            </div>
          </div>
          <div class="col-md-1">
            <button id="playBtn" class="btn btn-primary  btn-lg" style="margin-top: 7px;margin-left: -17px;" v-on:click="animation"><font-awesome-icon icon="play" class="ml-1"/></button>
          </div> 
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import vueSlider from 'vue-slider-component';
import * as d3 from 'd3';
import simpleheat from 'simpleheat';
// import Chart from 'chart.js';
const manhattanPrecinctMap = require("./manhattan_precinct_map.vue").default;
const tooltip = require("./tooltip.vue").default;

const manhattan_precinct = ["1", "5", "6", "7", "9", "10", "13", "14", "17", "18", "19", "20", "22", "23", "24", "25", "26", "28", "30", "32", "33", "34"];

// 0:downtown 1:midtown 2: uptown 3: uppertown   -- according to wiki(https://en.wikipedia.org/wiki/List_of_Manhattan_neighborhoods) and google map (search midtown manhattan)
const precinct_area_map = {"1": 0, "5":0, "6":0, "7":0, "9":0, 
                           "10":1, "13":1, "14":1, "17":1, "18":1, 
                           "19":2, "20":2, "22":2, "23":3, "24":2, 
                           "25":3, "26":3, "28":3, "30":3, "32":3, "33":3, "34":3}

export default {
  components: {
    ManhattanPrecinctMap: manhattanPrecinctMap,
    Tooltip: tooltip,
    vueSlider,
  },
  name: 'statistic-plot-page',
  data: function() {
    return {
      title: 'Statistic Plot',

      // Commom
      currDay: 2,
      currHour: 1,
      currPrecinct: undefined,
      mapIsReady: false,

      // Criminal and traffic data
      combine_data: undefined,
      maxNbCriminal: 0,
      maxNbTraffic: 0,
      data1Ready: false,
      criminalChart: undefined,
      trafficChart: undefined,
      
      curr_crime: undefined,
      max_crime: undefined,
      min_crime: undefined,
      max_crime_time: undefined,
      min_crime_time: undefined,
      max_crime_change: undefined,

      curr_traffic: undefined,
      max_traffic: undefined,
      min_traffic: undefined,
      max_traffic_time: undefined,
      min_traffic_time: undefined,
      max_traffic_change: undefined,

      // Sentiment Data
      sentiment_data: undefined,
      data2Ready: false,
      sentimentPosChart: undefined,
      sentimentNegChart: undefined,

      curr_positive: undefined,
      min_positive: undefined,
      max_positive: undefined,
      min_positive_time: undefined,
      max_positive_time: undefined,
      max_positive_change: undefined,

      // Correlation
      correlation_data: undefined,
      data3_ready: false,
      max_pearson: undefined,
      min_pearson: undefined,
      max_kendall: undefined,
      min_kendall: undefined,
      max_spearman: undefined,
      min_spearman: undefined,
      max_pearson_time: undefined,
      min_pearson_time: undefined,
      max_kendall_time: undefined,
      min_kendall_time: undefined,
      max_spearman_time: undefined,
      min_spearman_time: undefined,

      // Utils
      /// Day slider
      dayIndexMap:{"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6},
      hourSliderValue: 12,
      daySliderValue: "THU",
      daySliderOption:{
        width: 'auto',
        tooltip: "hover",
        disable: false,
        piecewise: true,
        piecewiseLabel: true,
        startAnimation: false,
        data: ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"],
        speed: 0.1,
      },

      /// Hour Slider
      hourSliderOption:{
        width: 'auto',
        tooltip: "hover",
        disable: false,
        piecewise: true,
        piecewiseLabel: true,
        startAnimation: false,
        data: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        speed: 0.1,
      },
    }
  },
  created: function(){
    var that = this;

    that.combine_data = {};
    var count1 = 0;
    d3.csv("static/data/statistic_crime_and_traffic.csv", function(data) {
      if(manhattan_precinct.includes(data.precinct) == true){
        var total_criminal = +data.criminal;
        var total_traffic = +data.traffic;
        if(that.maxNbCriminal < total_criminal){
          that.maxNbCriminal = total_criminal;
        }
        if(that.maxNbTraffic < total_traffic){
          that.maxNbTraffic = total_traffic;
        }
        if(that.combine_data[+data.day] === undefined){
          that.combine_data[+data.day] = {}
        }
        if(that.combine_data[+data.day][+data.precinct] === undefined){
          that.combine_data[+data.day][+data.precinct] = {}
        }

        that.combine_data[+data.day][+data.precinct][+data.hour] = {
          "precinct": +data.precinct, 
          "criminal": total_criminal,
          "traffic": total_traffic,
          "population": +data.population,
          "age": +data.age,
          "area": precinct_area_map[data.precinct],
          "max_crime": +data.max_crime,
          "min_crime": +data.min_crime,
          "max_crime_time": +data.max_crime_time,
          "min_crime_time": +data.min_crime_time,
          "max_crime_change": +data.max_crime_change,
          "min_traffic": +data.min_traffic,
          "max_traffic": +data.max_traffic,
          "min_traffic_time": +data.min_traffic_time,
          "max_traffic_time": +data.max_traffic_time,
          "max_traffic_change": +data.max_traffic_change
        };
      }

      count1++;

      if(count1 >=  7*24*76){
        that.data1Ready = true;
        that.onDataReady();
      }
    });

    var count2 = 0;
    that.sentiment_data = {};
    d3.csv("static/data/statistic_sentiment.csv", function(data){
      if(that.sentiment_data[+data.day] === undefined){
        that.sentiment_data[+data.day] = {};
      }
      if(that.sentiment_data[+data.day][+data.hour] === undefined){
        that.sentiment_data[+data.day][+data.hour] = {}
      }
      that.sentiment_data[+data.day][+data.hour]["negative"] = +data.negative;
      that.sentiment_data[+data.day][+data.hour]["positive"] = +data.positive;
      that.sentiment_data[+data.day][+data.hour]["min_positive"] = +data.min_positive;
      that.sentiment_data[+data.day][+data.hour]["max_positive"] = +data.max_positive;
      that.sentiment_data[+data.day][+data.hour]["min_positive_time"] = +data.min_positive_time;
      that.sentiment_data[+data.day][+data.hour]["max_positive_time"] = +data.max_positive_time;
      that.sentiment_data[+data.day][+data.hour]["max_positive_change"] = +data.max_positive_change;

      count2++;
      if(count2 >= 7 * 24){
        that.data2Ready = true;
        that.onDataReady();
      }
    });

    var count3 = 0;
    that.correlation_data = {};
    d3.csv("static/data/statistic_correlation.csv", function(data){
      if(that.correlation_data[+data.day] === undefined){
        that.correlation_data[+data.day] = {};
      }
      if(that.correlation_data[+data.day][+data.hour] === undefined){
        that.correlation_data[+data.day][+data.hour] = {}
      }
      that.correlation_data[+data.day][+data.hour]["pearson"] = +data.pearson;
      that.correlation_data[+data.day][+data.hour]["kendall"] = +data.kendall;
      that.correlation_data[+data.day][+data.hour]["spearman"] = +data.spearman;

      that.correlation_data[+data.day][+data.hour]["max_pearson_val"] = +data.max_pearson_val;
      that.correlation_data[+data.day][+data.hour]["min_pearson_val"] = +data.min_pearson_val;
      that.correlation_data[+data.day][+data.hour]["max_pearson_time"] = +data.max_pearson_time;
      that.correlation_data[+data.day][+data.hour]["min_pearson_time"] = +data.min_pearson_time;

      that.correlation_data[+data.day][+data.hour]["max_kendall_val"] = +data.max_kendall_val;
      that.correlation_data[+data.day][+data.hour]["min_kendall_val"] = +data.min_kendall_val;
      that.correlation_data[+data.day][+data.hour]["max_kendall_time"] = +data.max_kendall_time;
      that.correlation_data[+data.day][+data.hour]["min_kendall_time"] = +data.min_kendall_time;

      that.correlation_data[+data.day][+data.hour]["max_spearman_val"] = +data.max_spearman_val;
      that.correlation_data[+data.day][+data.hour]["min_spearman_val"] = +data.min_spearman_val;
      that.correlation_data[+data.day][+data.hour]["max_spearman_time"] = +data.max_spearman_time;
      that.correlation_data[+data.day][+data.hour]["min_spearman_time"] = +data.min_spearman_time;

      count3++;
      if(count3 >= 7 * 24){
        that.data3Ready = true;
        that.onDataReady();
      }
    });
  },
  mounted: function(){
    var that = this;

  },
  computed:{
    currentPrecinctTitle: function(){
      return "Precinct: " + this.currPrecinct;
    },
  },
  watch: {
    hourSliderValue: function() {
      var that = this;
      that.currHour = +that.hourSliderValue;
      that.updateStatisticData();
    },
    daySliderValue: function() {
      var that = this;
      that.currDay = +that.dayIndexMap[that.daySliderValue];

      if(that.criminalChart !== undefined){
        that.criminalChart.destroy();
      }
      if(that.trafficChart !== undefined){
        that.trafficChart.destroy();
      }
      if(that.sentimentPosChart){
        that.sentimentPosChart.destroy();
      }
      if(that.sentimentNegChart){
        that.sentimentNegChart.destroy();
      }

      that.updateStatisticData();
      that.createCrimeChart();
      that.createTrafficChart();
      that.createSentimentChart();
      that.createCorrelationChart();
    },
    currPrecinct: function(){
      var that = this;
      if(that.criminalChart !== undefined){
        that.criminalChart.destroy();
      }
      if(that.trafficChart !== undefined){
        that.trafficChart.destroy();
      }
      if(that.sentimentPosChart){
        that.sentimentPosChart.destroy();
      }
      if(that.sentimentNegChart){
        that.sentimentNegChart.destroy();
      }

      that.updateStatisticData();
      that.createCrimeChart();
      that.createTrafficChart();
      that.createSentimentChart();
      that.createCorrelationChart();
    },
  },
  methods: {
    onDataReady: function(){
      if(this.data1Ready == true && this.data2Ready == true && this.data3Ready == true && this.mapIsReady == true){
        this.$refs.hourSlider.setIndex(0);
        this.$refs.daySlider.setIndex(0);
        d3.select(".nb1").dispatch("click");
        setTimeout(function(){
          d3.select(".nb1").dispatch("mouseout")
        }, 
        1000);
      }
    },
    pad: function(num, size) {
        var s = "000000000" + num;
        return s.substr(s.length-size);
    },
    onPrecinctSelected: function(precinctIdx) {
      this.currPrecinct = precinctIdx;
    },
    onPrecinctDeselected: function(stateCode) {
      // this.currPrecinct = undefined;
    },
    onMapIsReady: function(signal){
      this.mapIsReady = true;
      this.onDataReady();
    },
    getCombineDayData : function(dayIdx, contentIdx, precinctIdx){
      var that = this;
      var data = [];
      for(var i = 0; i < 24; i++){
        data.push(that.combine_data[dayIdx][precinctIdx][i][contentIdx])
      }
      return data;
    },
    getSentimentDayData : function(dayIdx, contentIdx){
      var that = this;
      var data = [];
      for(var i = 0; i < 24; i++){
        data.push(that.sentiment_data[dayIdx][i][contentIdx])
      }
      return data;
    },
    getCorrelationDayDate : function(dayIdx, contentIdx){
      var that = this;
      var data = [];
      for(var i = 0; i < 24; i++){
        data.push(that.correlation_data[dayIdx][i][contentIdx])
      }
      return data;
    },
    createCrimeChart: function(){
      var that = this;
      var canvas = document.getElementById("crimeLineCanvas");
      that.criminalChart = new Chart(canvas, {
        type: 'line',
        data: {
          labels: ["0h","1h","2h","3h","4h","5h","6h","7h","8h","9h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h"],
          datasets: [{ 
              data: that.getCombineDayData(that.currDay, "criminal", that.currPrecinct),
              label: "# of crime",
              borderColor: "#3e95cd",
              fill: true
            },
          ]
        },
        options: {
          animation: {
            duration: 0, // general animation time
          },
          legend: {
            display: true
          },
          tooltips: {
            enabled: true
          }
        }
      });
    },
    createTrafficChart: function(){
      var that = this;
      var canvas = document.getElementById("trafficLineCanvas");
      that.trafficChart = new Chart(canvas, {
        type: 'line',
        data: {
          labels: ["0h","1h","2h","3h","4h","5h","6h","7h","8h","9h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h"],
          datasets: [{ 
              data: that.getCombineDayData(that.currDay, "traffic", that.currPrecinct),
              label: "# of commuter",
              borderColor: "#3e95cd",
              fill: true
            },
          ]
        },
        options: {
          animation: {
            duration: 0, // general animation time
          },
          legend: {
            display: true
          },
          tooltips: {
            enabled: true
          }
        }
      });
    },
    createSentimentChart: function(){
      var that = this;
      var canvas = document.getElementById("sentimentLineCanvas");
      that.sentimentPosChart = new Chart(canvas, {
        type: 'line',
        data: {
          labels: ["0h","1h","2h","3h","4h","5h","6h","7h","8h","9h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h"],
          datasets: [{ 
              data: that.getSentimentDayData(that.currDay, "positive"),
              borderColor: "#3e95cd",
              label: "Positive (%)",
              fill: true
            },{ 
              data: that.getSentimentDayData(that.currDay, "negative"),
              borderColor: "#8e5ea2",
              label: "Negative (%)",
              fill: true
            },
          ]
        },
        options: {
          animation: {
            duration: 0, // general animation time
          },
          legend: {
              display: true
          },
          tooltips: {
              enabled: true
          }
        }
      });
    },
    createCorrelationChart: function(){
      var that = this;
      var canvas = document.getElementById("correlationLineCanvas");
      that.sentimentNegChart = new Chart(canvas, {
        type: 'line',
        data: {
          labels: ["0h","1h","2h","3h","4h","5h","6h","7h","8h","9h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h"],
          datasets: [{ 
              data: that.getCorrelationDayDate(that.currDay, "pearson"),
              label: "pearson",
              borderColor: "#3e95cd",
              fill: true
            },{ 
              data: that.getCorrelationDayDate(that.currDay, "kendall"),
              label: "kendall",
              borderColor: "#8e5ea2",
              fill: true
            },{ 
              data: that.getCorrelationDayDate(that.currDay, "spearman"),
              label: "spearman",
              borderColor: "#3cba9f",
              fill: true
            },
          ]
        },
        options: {
          animation: {
            duration: 0, // general animation time
          },
          legend: {
              display: true
          },
          tooltips: {
              enabled: true
          }
        }
      });
    },
    updateStatisticData: function(){
      var that = this;
      // Crime data
      that.curr_crime = that.combine_data[that.currDay][that.currPrecinct][that.currHour]["criminal"];
      that.max_crime = that.combine_data[that.currDay][that.currPrecinct][that.currHour]["max_crime"];
      that.min_crime = that.combine_data[that.currDay][that.currPrecinct][that.currHour]["min_crime"];
      that.max_crime_time = that.combine_data[that.currDay][that.currPrecinct][that.currHour]["max_crime_time"];
      that.min_crime_time = that.combine_data[that.currDay][that.currPrecinct][that.currHour]["min_crime_time"];
      that.max_crime_change = that.combine_data[that.currDay][that.currPrecinct][that.currHour]["max_crime_change"];

      // Traffic data
      that.curr_traffic = that.combine_data[that.currDay][that.currPrecinct][that.currHour]["traffic"];
      that.max_traffic = that.combine_data[that.currDay][that.currPrecinct][that.currHour]["max_traffic"];
      that.min_traffic = that.combine_data[that.currDay][that.currPrecinct][that.currHour]["min_traffic"];
      that.max_traffic_time = that.combine_data[that.currDay][that.currPrecinct][that.currHour]["max_traffic_time"];
      that.min_traffic_time = that.combine_data[that.currDay][that.currPrecinct][that.currHour]["min_traffic_time"];
      that.max_traffic_change = that.combine_data[that.currDay][that.currPrecinct][that.currHour]["max_traffic_change"];

      //Sentiment Data
      that.curr_positive = that.sentiment_data[that.currDay][that.currHour]["positive"];
      that.max_positive = that.sentiment_data[that.currDay][that.currHour]["max_positive"];
      that.min_positive = that.sentiment_data[that.currDay][that.currHour]["min_positive"];
      that.max_positive_time = that.sentiment_data[that.currDay][that.currHour]["max_positive_time"];
      that.min_positive_time = that.sentiment_data[that.currDay][that.currHour]["min_positive_time"];
      that.max_positive_change = that.sentiment_data[that.currDay][that.currHour]["max_positive_change"];

      //Correlation Data
      that.min_pearson = that.correlation_data[that.currDay][that.currHour]["min_pearson_val"].toFixed(2);
      that.max_pearson = that.correlation_data[that.currDay][that.currHour]["max_pearson_val"].toFixed(2);
      that.min_kendall = that.correlation_data[that.currDay][that.currHour]["min_kendall_val"].toFixed(2);
      that.max_kendall = that.correlation_data[that.currDay][that.currHour]["max_kendall_val"].toFixed(2);
      that.min_spearman = that.correlation_data[that.currDay][that.currHour]["min_spearman_val"].toFixed(2);
      that.max_spearman = that.correlation_data[that.currDay][that.currHour]["max_spearman_val"].toFixed(2);

      that.min_pearson_time = that.pad(that.correlation_data[that.currDay][that.currHour]["min_pearson_time"], 2);
      that.max_pearson_time = that.pad(that.correlation_data[that.currDay][that.currHour]["max_pearson_time"], 2);
      that.min_kendall_time = that.pad(that.correlation_data[that.currDay][that.currHour]["min_kendall_time"], 2);
      that.max_kendall_time = that.pad(that.correlation_data[that.currDay][that.currHour]["max_kendall_time"], 2);
      that.min_spearman_time = that.pad(that.correlation_data[that.currDay][that.currHour]["min_spearman_time"], 2);
      that.max_spearman_time = that.pad(that.correlation_data[that.currDay][that.currHour]["max_spearman_time"], 2);
    },
    animation: function(){
      var that = this;
      var pauseSec = 1000;
      that.animationSet1(0, pauseSec)
    },
    animationSet1: function(day, pauseSec){
      var that = this;
      that.$refs.daySlider.setIndex(day);
      if(day >= 6){
        return;
      }
      setTimeout(function(){
        day += 1;
        that.animationSet1(day, pauseSec);
      }, pauseSec);
    },
  },
}
</script>

<style>


.cliente {
  border: #cdcdcd medium solid;
  border-radius: 10px;
  -moz-border-radius: 10px;
  -webkit-border-radius: 10px;
}


#playBtn{
  border: 1px solid black;
  border-radius: 50%;
}

#app{
  margin-top: 20px;
}

#crimeDataText {
  display: block;
}

#dataContainer{
  left: -125px;
  line-height: 16px;
  padding: 10px;
  background: rgba(255,255,255,0.9);
  color: #000;
  box-shadow: 0 1px 5px rgba(0,0,0,0.4);
  -moz-box-shadow: 0 1px 5px rgba(0,0,0,0.4);
  text-align:center;
  -moz-border-radius: 10px;
  -webkit-border-radius: 10px;
  font-size: 15px;
}
</style>