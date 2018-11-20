<template>
    <div class="criminalMap">
      <h1>{{title}}</h1>
      <div class="container">
        <div class="mapHolder">
          <NewyorkMap
            @precinctSelected="onPrecinctSelected"
            @precinctDeselected="onPrecinctDeselected"
            @mapIsReady="onMapIsReady"
          />
        </div>
        <div class="tooltipHolder">
          <Tooltip
            v-if="currPrecinct"
            :title="currentPrecinctTitle"
            :description="currentPrecinctDescription"
          />
        </div>
        <div class="sliderHolder">
          <vue-slider 
            ref="hourSlider"
            v-model="hourSliderValue"
            v-bind="hourSliderOption"
          >
          </vue-slider>
          <vue-slider 
            ref="daySlider"
            v-model="daySliderValue"
            v-bind="daySliderOption"
          >
          </vue-slider>
        </div>
        <button v-on:click="animation">animation</button>

        <div>
          <img :src="sentimentEmoji" alt="img">
        </div>
      </div>
    </div>
</template>

<script>
import vueSlider from 'vue-slider-component';
import * as d3 from 'd3';

const newyorkMap = require("./newyork_map.vue").default;
const tooltip = require("./tooltip.vue").default;

export default {
  components: {
    NewyorkMap: newyorkMap,
    Tooltip: tooltip,
    vueSlider,
  },
  name: 'Map Plot Page',
  data: function() {
    return {
      title: 'Criminal Map',
      criminalData: undefined,
      trafficFlowData: undefined,
      senmentimentData: undefined,

      currPrecinct: undefined,
      currDay: 2,
      currHour: 1,
      maxNbCriminal: 0,
      maxNbTraffic: 0,
      hourSliderValue: undefined,
      daySliderValue: undefined,

      sentimentEmoji: undefined,
      sentimentEmojis: [
        "static/images/1.png",
        "static/images/2.png",
        "static/images/3.png",
        "static/images/4.png",
        "static/images/5.png",
      ],

      daySliderOption:{
        width: 'auto',
        tooltip: "always",
        disable: false,
        piecewise: true,
        piecewiseLabel: true,
        startAnimation: true,
        data: [0, 1, 2, 3, 4, 5, 6]
      },
      hourSliderOption:{
        width: 'auto',
        tooltip: "always",
        disable: false,
        piecewise: true,
        piecewiseLabel: true,
        startAnimation: true,
        data: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
      }
    }
  },
  created: function(){
    console.log("created")
    var that = this;

    that.criminalData = {};
    d3.csv("static/data/NYPD_crime_daily_aggregation.csv", function(data) {
      if(that.maxNbCriminal < +data.totalNumber){
        that.maxNbCriminal = +data.totalNumber;
      }
      if(that.criminalData[+data.day] === undefined){
        that.criminalData[+data.day] = {}
      }

      if(that.criminalData[+data.day][+data.hour] === undefined){
        that.criminalData[+data.day][+data.hour] = {}
      }
      
      if(that.criminalData[+data.day][+data.hour][+data.precinct] === undefined){
        that.criminalData[+data.day][+data.hour][+data.precinct] = 0
      }
      
      that.criminalData[+data.day][+data.hour][+data.precinct] = +data["totalNumber"];
      }
    );

    that.trafficFlowData = {};
    d3.csv("static/data/final_table_complete_subset.csv", function(data){ 
      var total = +data.HOURLY_ENTRIES + (+data.HOURLY_EXITS);
      if(that.maxNbTraffic < +total){
        that.maxNbTraffic = +total;
      }
      if(that.trafficFlowData[+data.Month] === undefined){
        that.trafficFlowData[+data.Month] = {}
      }

      if(that.trafficFlowData[+data.Month][+data.HOUR_modified] === undefined){
        that.trafficFlowData[+data.Month][+data.HOUR_modified] = {}
      }

      that.trafficFlowData[+data.Month][+data.HOUR_modified][(data.Latitude + ":" +data.Longitude)] = total;
    });

    that.senmentimentData = {};
    var fakeData = {
      1:{
        0:{"Sentiment": -1.0  },
        1:{"Sentiment": -0.9  },
        2:{"Sentiment": -0.8  },
        3:{"Sentiment": -0.7  },
        4:{"Sentiment": -0.6  },
        5:{"Sentiment": -0.55 },
        6:{"Sentiment": -0.54 },
        7:{"Sentiment": -0.53 },
        8:{"Sentiment": -0.52 },
        9:{"Sentiment": -0.51 },
        10:{"Sentiment": -0.5 },
        11:{"Sentiment": -0.49},
        12:{"Sentiment": -0.48},
        13:{"Sentiment": -0.4 },
        14:{"Sentiment": -0.3 },
        15:{"Sentiment": -0.2 },
        16:{"Sentiment": -0.1 },
        17:{"Sentiment": -0.05},
        18:{"Sentiment": 0.01 },
        19:{"Sentiment": 0.0  },
        20:{"Sentiment": 0.05 },
        21:{"Sentiment": 0.1  },
        22:{"Sentiment": 0.2  },
        23:{"Sentiment": 0.3  }
      },
      2:{
        0:{"Sentiment": 0.35 },
        1:{"Sentiment": 0.4  },
        2:{"Sentiment": 0.45 },
        3:{"Sentiment": 0.46 },
        4:{"Sentiment": 0.47 },
        5:{"Sentiment": 0.48 },
        6:{"Sentiment": 0.49 },
        7:{"Sentiment": 0.50 },
        8:{"Sentiment": 0.51 },
        9:{"Sentiment": 0.52 },
        10:{"Sentiment": 0.53},
        11:{"Sentiment": 0.6 },
        12:{"Sentiment": 0.7 },
        13:{"Sentiment": 0.8 },
        14:{"Sentiment": 0.9 },
        15:{"Sentiment": 0.91},
        16:{"Sentiment": 0.92},
        17:{"Sentiment": 0.93},
        18:{"Sentiment": 0.94},
        19:{"Sentiment": 0.95},
        20:{"Sentiment": 0.97},
        21:{"Sentiment": 0.98},
        22:{"Sentiment": 0.99},
        23:{"Sentiment": 1.0 }
      },
    };
    // d3.csv("static/data/sentiment.csv", function(data){
    // });
    that.senmentimentData = fakeData;
  },
  computed:{
    currentPrecinctTitle: function(){
      return "Precinct: " + this.currPrecinct;
    },
    currentPrecinctDescription: function(){
      return "Number of Crime: " + this.criminalData[this.currDay][this.currHour][this.currPrecinct];
    },
  },
  watch: {
    hourSliderValue: {
      handler: function(){
        console.log("hour sliderValue change")
        var that = this;
        that.currHour = +that.hourSliderValue;
        const quantize = d3.scaleQuantize()
                            .domain([0, that.maxNbCriminal])
                            .range(d3.range(9).map(i => "q" + i));

        var svg = d3.select("svg");
        var selections = svg.selectAll(".precinct");
        selections.each(function() {
          var s = d3.select(this);
          var precinctFullContext = s.attr("class")
          var precinctContext = precinctFullContext.split(" ")[0];
          var precinctSuffix = precinctFullContext.split(" ")[1];
          var precinctNum = precinctContext.substring(2, precinctContext.length);
          s.attr("class", precinctContext + " " + precinctSuffix + " " + quantize(that.criminalData[that.currDay][that.currHour][+precinctNum]))
        });
        this.updateCriminalDataBar();
        this.updateTrafficFlow();
        this.updateSentiment();
      }
    },
    daySliderValue: {
      handler: function(){
        console.log("day slider Value change")
        var that = this;
        that.currDay = +that.daySliderValue;
        const quantize = d3.scaleQuantize()
                            .domain([0, that.maxNbCriminal])
                            .range(d3.range(9).map(i => "q" + i));

        var svg = d3.select("svg");
        var selections = svg.selectAll(".precinct");
        selections.each(function() {
          var s = d3.select(this);
          var precinctFullContext = s.attr("class")
          var precinctContext = precinctFullContext.split(" ")[0];
          var precinctSuffix = precinctFullContext.split(" ")[1];
          var precinctNum = precinctContext.substring(2, precinctContext.length);
          s.attr("class", precinctContext + " " + precinctSuffix + " " + quantize(that.criminalData[that.currDay][that.currHour][+precinctNum]))
        });
        this.updateCriminalDataBar();
        this.updateTrafficFlow();
        this.updateSentiment();
      }
    },
    immediate: true,
  },
  methods: {
    onPrecinctSelected: function(precinctIdx) {
      this.currPrecinct = precinctIdx;
    },
    onPrecinctDeselected: function(stateCode) {
      this.currPrecinct = undefined;
    },
    onMapIsReady: function(signal){
      this.$refs.hourSlider.setIndex(0);
      this.$refs.daySlider.setIndex(0);
    },
    updateCriminalDataBar: function(){
      var that = this;
      var svg = d3.select(".mapHolder")
      svg = svg.select("svg")
      var width = +svg.attr('width');
      var height = +svg.attr('height');
      const projection = d3.geoMercator()
                           .center([-73.94, 40.70])
                           .scale(50000)
                           .translate([width/2, height/2]);

      var bars = svg.selectAll(".bars");
      bars.each(function(){
        var bar = d3.select(this);
        var precinctNum = bar.attr("class").split(" ")[1];

        bar.select("rect")
          .attr('height', function() {
            return that.criminalData[that.currDay][that.currHour][precinctNum];
          })
          .attr('width', 3)
          .attr('y', function() {
            return -that.criminalData[that.currDay][that.currHour][precinctNum];
          })
          .attr("class", "bars")
          .style("fill", "blue")
          .style("stroke", "white")
          .style("stroke-width", 0.5)
          .style("opacity", 0.7);
      })
    },
    updateTrafficFlow: function(){
      var that = this;
      var svg = d3.select(".mapHolder")
      svg = svg.select("svg")
      var width = +svg.attr('width');
      var height = +svg.attr('height');
      const projection = d3.geoMercator()
                          .center([-73.94, 40.70])
                          .scale(50000)
                          .translate([width/2, height/2]);

      var keys = Object.keys(that.trafficFlowData[that.currDay][that.currHour])
      
      d3.selectAll("circle")
        .remove();
      keys.forEach(function(key){
        var lat = +key.split(":")[0];
        var long = +key.split(":")[1];
        var coord = projection([long, lat])

        svg.append('circle')
            .attr('cx', coord[0])
            .attr('cy', coord[1])
            .attr('r', +that.trafficFlowData[that.currDay][that.currHour][key] / that.maxNbCriminal * 0.1);
      })

     var test = projection([-73.94, 40.70])
      svg.append('svg:circle')
          .attr('cx', test[0])
          .attr('cy', test[1])
          .attr('r', 3);
    },
    updateSentiment: function(){
      var that = this;
      var sentimentValue =  that.senmentimentData[that.currDay][that.currHour]["Sentiment"]

      if(sentimentValue >= -1.0 && sentimentValue < -0.75){
        that.sentimentEmoji = that.sentimentEmojis[4];
      }
      else if(sentimentValue >= -0.75 && sentimentValue < -0.25){
        that.sentimentEmoji = that.sentimentEmojis[3];
      }
      else if(sentimentValue >= -0.25 && sentimentValue < 0.25){
        that.sentimentEmoji = that.sentimentEmojis[2];
      }
      else if(sentimentValue >= 0.25 && sentimentValue < 0.75){
        that.sentimentEmoji = that.sentimentEmojis[1];
      }
      else if(sentimentValue >= 0.75 && sentimentValue < 1.0){
        that.sentimentEmoji = that.sentimentEmojis[0];
      }
    },
    animation: function(){
      var that = this;
      var pauseSec = 250;
      // that.animationHour(0, pauseSec);
      // that.animationDay(0, pauseSec);
      that.animationSet1(1, 0, pauseSec)
    },
    animationSet1: function(day, hour, pauseSec){
      var that = this;
      console.log(day, hour )
      that.$refs.hourSlider.setValue(hour);
      that.$refs.daySlider.setValue(day);
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
    animationDay: function(dayIdx, pauseSec){
      var that = this;
      if(dayIdx <= 12){
        setTimeout(function(){
          that.$refs.daySlider.setValue(dayIdx);
          dayIdx += 1;
          that.animationDay(dayIdx, pauseSec);
        }, pauseSec);
      }
    },
    animationHour: function(hourIdx, pauseSec){
      var that = this;
      if(hourIdx < 24){
        setTimeout(function(){
          that.$refs.hourSlider.setValue(hourIdx);
          hourIdx += 1;
          that.animationHour(hourIdx, pauseSec);
        }, pauseSec);
      }
    },
  },
}
</script>

<style>
.criminalMap{
}

.mapHolder {
}

.tooltipHolder{

}
img{
  width: 500px;
  height: 500px;
}
circle{
	fill: green;
  opacity: 0.8;
  fill-opacity: .5;
}
.q0 { fill:rgb(247,251,255) }
.q1 { fill:rgb(222,235,247) }
.q2 { fill:rgb(198,219,239) }
.q3 { fill:rgb(158,202,225) }
.q4 { fill:rgb(107,174,214) }
.q5 { fill:rgb(66,146,198) }
.q6 { fill:rgb(33,113,181) }
.q7 { fill:rgb(8,81,156) }
.q8 { fill:rgb(8,48,107) }
</style>