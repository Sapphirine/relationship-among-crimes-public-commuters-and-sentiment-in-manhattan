<template>
  <div class="statisticPlot">
    <div class="container-fluid">
      <div class="statisticInfoHolder" style="margin-left: 15px;margin-right: 4px;" >
        <div class="row">
          <div class="col-sm-3 " >
            <div class="mapHolder cliente">
              <NewyorkMap
                @precinctSelected="onPrecinctSelected"
                @precinctDeselected="onPrecinctDeselected"
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
                  <div class="">Current # of Crime: </div>
                  <div class="">Minimal # of Crime: </div>
                  <div class="">Maximal # of Crime: </div>
                  <div class="">Maximal # of Crime :  </div>
                  <div class="">1</div>
                  <div class="">2</div>
                </div>
              </div>
            </div>

            <div class="my-3">
            </div>
            <div class="card cliente">
              <div id="title">
                <h4>Traffic Trend</h4>
              </div>
              <canvas id="trafficLineCanvas"></canvas>
              <div id="crimeDataText">
                <div id="dataContainer">
                  <div class="">1</div>
                  <div class="">2</div>
                  <div class="">1</div>
                  <div class="">2</div>
                  <div class="">1</div>
                  <div class="">2</div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-sm-3">
            <div class="card cliente">
              <div id="title">
                <h4>Positive Sentiment Trend</h4>
              </div>
              <canvas id="sentimentPositiveLineCanvas"></canvas>
              <div id="sentimentPosDataText">
                <div id="dataContainer">
                  <div class="">1</div>
                  <div class="">2</div>
                  <div class="">1</div>
                  <div class="">2</div>
                  <div class="">1</div>
                  <div class="">2</div>
                </div>
              </div>
            </div>
            <div class="my-3">
            </div>
            <div class="card cliente">
              <div id="title">
                <h4>Negative Sentiment Trend</h4>
              </div>
              <canvas id="sentimentNegativeLineCanvas"></canvas>
              <div id="sentimentNegDataText">
                <div id="dataContainer">
                  <div class="">1</div>
                  <div class="">2</div>
                  <div class="">1</div>
                  <div class="">2</div>
                  <div class="">1</div>
                  <div class="">2</div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-sm-3">
            <div class="card cliente">
              <div id="title">
                <h4>Positive Sentiment Trend</h4>
              </div>
              <canvas id="sentimentPositiveLineCanvas"></canvas>
              <div id="sentimentPosDataText">
                <div id="dataContainer">
                  <div class="">1</div>
                  <div class="">2</div>
                  <div class="">1</div>
                  <div class="">2</div>
                  <div class="">1</div>
                  <div class="">2</div>
                </div>
              </div>
            </div>
            <div class="my-3">
            </div>
            <div class="card cliente">
              <div id="title">
                <h4>Negative Sentiment Trend</h4>
              </div>
              <canvas id="sentimentNegativeLineCanvas"></canvas>
              <div id="sentimentNegDataText">
                <div id="dataContainer">
                  <div class="">1</div>
                  <div class="">2</div>
                  <div class="">1</div>
                  <div class="">2</div>
                  <div class="">1</div>
                  <div class="">2</div>
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
const newyorkMap = require("./newyork_map.vue").default;
const tooltip = require("./tooltip.vue").default;

const manhattan_precinct = ["1", "5", "6", "7", "9", "10", "13", "14", "17", "18", "19", "20", "22", "23", "24", "25", "26", "28", "30", "32", "33", "34"];

// 0:downtown 1:midtown 2: uptown 3: uppertown   -- according to wiki(https://en.wikipedia.org/wiki/List_of_Manhattan_neighborhoods) and google map (search midtown manhattan)
const precinct_area_map = {"1": 0, "5":0, "6":0, "7":0, "9":0, 
                           "10":1, "13":1, "14":1, "17":1, "18":1, 
                           "19":2, "20":2, "22":2, "23":3, "24":2, 
                           "25":3, "26":3, "28":3, "30":3, "32":3, "33":3, "34":3}

export default {
  components: {
    NewyorkMap: newyorkMap,
    Tooltip: tooltip,
    vueSlider,
  },
  name: 'statistic-plot-page',
  data: function() {
    return {
      title: 'MISC Plot',

      // Commom
      currDay: 2,
      currHour: 1,
      currPrecinct: undefined,

      // Criminal and traffic data
      combine_data: undefined,
      maxNbCriminal: 0,
      maxNbTraffic: 0,
      data1Ready: false,
      criminalChart: undefined,
      trafficChart: undefined,

      // Sentiment Data
      sentiment_data: undefined,
      data2Ready: false,
      sentimentPosChart: undefined,
      sentimentNegChart: undefined,

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
        data: ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
      },

      /// Hour Slider
      hourSliderOption:{
        width: 'auto',
        tooltip: "hover",
        disable: false,
        piecewise: true,
        piecewiseLabel: true,
        startAnimation: false,
        data: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
      },
    }
  },
  created: function(){
    var that = this;

    that.combine_data = {};
    var count1 = 0;
    d3.csv("static/data/chart_plot_combine_precinct.csv", function(data) {
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

        that.combine_data[+data.day][+data.precinct][+data.hour] = {"precinct": +data.precinct, "criminal": total_criminal, "traffic": total_traffic, "population": +data.population, "age": +data.age, "area": precinct_area_map[data.precinct]};
      }

      count1++;

      if(count1 >=  7*24*76){
        that.data1Ready = true;
        that.onDataReady();
      }
    });

    var count2 = 0;
    that.sentiment_data = {};
    d3.csv("static/data/sentiment_number.csv", function(data){
      if(that.sentiment_data[+data.day] === undefined){
        that.sentiment_data[+data.day] = {};
      }
      if(that.sentiment_data[+data.day][+data.hour] === undefined){
        that.sentiment_data[+data.day][+data.hour] = {}
      }
      that.sentiment_data[+data.day][+data.hour]["negative"] = +data.negative;
      that.sentiment_data[+data.day][+data.hour]["neutral"] = +data.neutral;
      that.sentiment_data[+data.day][+data.hour]["positive"] = +data.positive;

      count2++;
      if(count2 >= 7 * 24){
        that.data2Ready = true;
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
      // that.createCrimeChart();
      // that.createTrafficChart();
      // that.createSentimentPositiveChart();
      // that.createSentimentNegativeChart();
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

      that.createCrimeChart();
      that.createTrafficChart();
      that.createSentimentPositiveChart();
      that.createSentimentNegativeChart();
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

      that.createCrimeChart();
      that.createTrafficChart();
      that.createSentimentPositiveChart();
      that.createSentimentNegativeChart();
    },
  },
  methods: {
    onDataReady: function(){
      if(this.data1Ready == true && this.data2Ready == true){
        this.$refs.hourSlider.setIndex(0);
        this.$refs.daySlider.setIndex(0);
        this.currPrecinct = 1;
      }
    },
    onPrecinctSelected: function(precinctIdx) {
      this.currPrecinct = precinctIdx;
    },
    onPrecinctDeselected: function(stateCode) {
      // this.currPrecinct = undefined;
    },
    onMapIsReady: function(signal){
      // this.$refs.hourSlider.setIndex(0);
      // this.$refs.daySlider.setIndex(0);
    },
    getCombineDayData : function(dayIdx, contentIdx, precinctIdx){
      var that = this;
      var data = [];
      console.log(dayIdx, contentIdx, precinctIdx)
      console.log(that.combine_data[dayIdx])
      console.log(that.combine_data[dayIdx][precinctIdx])
      console.log(that.combine_data[dayIdx][precinctIdx][0])
      console.log(that.combine_data[dayIdx][precinctIdx][0][contentIdx])
      for(var i = 0; i < 24; i++){
        data.push(that.combine_data[dayIdx][precinctIdx][i][contentIdx])
      }
      return data;
    },
    getSentimentDayData : function(dayIdx, contentIdx){
      var that = this;
      var data = [];
      for(var i = 0; i < 24; i++){
        data.push(that.sentiment_data[dayIdx][i][contentIdx] / (that.sentiment_data[dayIdx][i]["negative"] + that.sentiment_data[dayIdx][i]["positive"] + that.sentiment_data[dayIdx][i]["neutral"]))
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
              borderColor: "#3e95cd",
              fill: true
            },
          ]
        },
        options: {
          legend: {
              display: false
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
              borderColor: "#3e95cd",
              fill: true
            },
          ]
        },
        options: {
          legend: {
              display: false
          },
          tooltips: {
              enabled: true
          }
        }
      });
    },
    createSentimentPositiveChart: function(){
      var that = this;
      var canvas = document.getElementById("sentimentPositiveLineCanvas");
      that.sentimentPosChart = new Chart(canvas, {
        type: 'line',
        data: {
          labels: ["0h","1h","2h","3h","4h","5h","6h","7h","8h","9h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h"],
          datasets: [{ 
              data: that.getSentimentDayData(that.currDay, "positive"),
              borderColor: "#3e95cd",
              fill: true
            },
          ]
        },
        options: {
          legend: {
              display: false
          },
          tooltips: {
              enabled: true
          }
        }
      });
    },
    createSentimentNegativeChart: function(){
      var that = this;
      var canvas = document.getElementById("sentimentNegativeLineCanvas");
      that.sentimentNegChart = new Chart(canvas, {
        type: 'line',
        data: {
          labels: ["0h","1h","2h","3h","4h","5h","6h","7h","8h","9h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h"],
          datasets: [{ 
              data: that.getSentimentDayData(that.currDay, "negative"),
              borderColor: "#3e95cd",
              fill: true
            },
          ]
        },
        options: {
          legend: {
              display: false
          },
          tooltips: {
              enabled: true
          }
        }
      });
    },
    animation: function(){
      var that = this;
      var pauseSec = 300;
      that.animationSet1(0, 0, pauseSec)
    },
    animationSet1: function(day, hour, pauseSec){
      var that = this;
      that.$refs.hourSlider.setIndex(hour);
      that.$refs.daySlider.setIndex(day);
      if(hour >= 24 && day >= 6){
        return;
      }
      setTimeout(function(){
        hour += 1;
        if(hour >= 24 && day < 6){
          hour = 0;
          day += 1;
        }
        that.animationSet1(day, hour, pauseSec);
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