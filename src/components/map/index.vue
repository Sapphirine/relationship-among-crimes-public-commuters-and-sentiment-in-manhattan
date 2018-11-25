<template>
  <div class="criminalMap">
    <canvas id="sentiment-chart" width="250" height="250"></canvas>

    <div class="container" style="width:1280px">

      <h1 style="position:absolute; top:3px; left:45%; color:white">{{title}}</h1>

      <div class="mapHolder">
        <ManhattanMap
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
      <div class="sliderHolder my-4 mb-2 pl-6">
        <div class="row">
          <div class="col-md-1">
          </div>
          <div class="col-md-1">
            <div class="row">
              <h5> <span class="badge badge-pill badge-primary ml-4 mr-1">Time </span> </h5>
            </div>
            <div class="row">
              <h5> <span class="badge badge-pill badge-primary ml-4 mr-1">Day </span> </h5>
            </div>
          </div>
          <div class="col-md-8">
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
            <button id="playBtn" class="btn btn-primary  btn-lg my-1" v-on:click="animation"><font-awesome-icon icon="play" /></button>
          </div> 
          <div class="col-md-1">
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

const chart = require("./donut_chart.js").default;
const manhattanMap = require("./manhattan_map.vue").default;
const tooltip = require("./tooltip.vue").default;

export default {
  components: {
    ManhattanMap: manhattanMap,
    Tooltip: tooltip,
    vueSlider,
  },
  name: 'map-plot-page',
  data: function() {
    return {
      title: 'Criminal Map',

      // Commom
      projection: undefined,
      currDay: 2,
      currHour: 1,

      // Criminal Data
      criminalData: undefined,
      precinctCenter: undefined,
      currPrecinct: undefined,
      maxNbCriminal: 0,
      
      // Traffic Data
      trafficFlowData: undefined,
      maxNbTraffic: 0,
      canvas_criminal: undefined,
      canvas_traffic: undefined,

      // Sentiment Data
      sentimentData: undefined,
      sentimentEmoji: undefined,
      sentimentEmojis: [
        "static/images/1.png",
        "static/images/2.png",
        "static/images/3.png",
        "static/images/4.png",
        "static/images/5.png",
      ],
      sentimentDonutChart: undefined,

      // Utils
      /// Day slider
      dayIndexMap:{"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6},
      hourSliderValue: undefined,
      daySliderValue: undefined,
      daySliderOption:{
        width: 'auto',
        tooltip: "hover",
        disable: false,
        piecewise: true,
        piecewiseLabel: true,
        startAnimation: true,
        data: ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
      },

      /// Hour Slider
      hourSliderOption:{
        width: 'auto',
        tooltip: "hover",
        disable: false,
        piecewise: true,
        piecewiseLabel: true,
        startAnimation: true,
        data: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
      },

      /// Donut chart
      donut_config: {
        type: 'doughnutLabels',
        data: {
          datasets: [{
            data: [
              1,2,1
            ],
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(75, 192, 192)',
            ],
            label: 'Sentiment'
          }],
          labels: [
            "Negative",
            "Neutral",
            "Positive"
          ]
        },
        options: {
          responsive: false,
          maintainAspectRatio: false,
          legend: {
            labels:{
              usePointStyle: true,
            },
            position: 'bottom',
          },
          title: {
            display: false,
            text: 'Sentiment'
          },
          animation: {
            animateScale: true,
            animateRotate: true
          },
        }
      },
    }
  },
  created: function(){
    console.log("created")
    var that = this;
      
    that.criminalData = {};
    //############# Aggreagtaion based on precinct area.
    // d3.csv("static/data/NYPD_crime_daily_aggregation.csv", function(data) {
    //   if(that.maxNbCriminal < +data.totalNumber){
    //     that.maxNbCriminal = +data.totalNumber;
    //   }
    //   if(that.criminalData[+data.day] === undefined){
    //     that.criminalData[+data.day] = {}
    //   }
    //   if(that.criminalData[+data.day][+data.hour] === undefined){
    //     that.criminalData[+data.day][+data.hour] = {}
    //   }
    //   if(that.criminalData[+data.day][+data.hour][+data.precinct] === undefined){
    //     that.criminalData[+data.day][+data.hour][+data.precinct] = 0
    //   }
    //   that.criminalData[+data.day][+data.hour][+data.precinct] = +data["totalNumber"];
    // });

    // that.precinctCenter = [];
    // d3.csv("static/data/precinct_center.csv", function(geoCenter) {
    //   var coord = that.projection([+geoCenter.long, +geoCenter.lat]);
    //   that.precinctCenter.push([coord[0], coord[1], +geoCenter.precinct]);
    // });

    //############# Aggreagtaion based on lat long.
    d3.csv("static/data/criminal_lat_long_001.csv", function(data) {
      var total = +data.sum;
      if(that.maxNbCriminal < total){
        that.maxNbCriminal = total;
      }
      if(that.criminalData[+data.day] === undefined){
        that.criminalData[+data.day] = {}
      }
      if(that.criminalData[+data.day][+data.hour] === undefined){
        that.criminalData[+data.day][+data.hour] = {}
      }
      that.criminalData[+data.day][+data.hour][(data.lat + ":" +data.long)] = total;
    });

    that.trafficFlowData = {};
    d3.csv("static/data/taxi_sort_001_clean.csv", function(data){ 
      var total = +data.sum;
      if(that.maxNbTraffic < +total){
        that.maxNbTraffic = +total;
      }
      if(that.trafficFlowData[+data.weekday] === undefined){
        that.trafficFlowData[+data.weekday] = {}
      }
      if(that.trafficFlowData[+data.weekday][+data.pick_hour] === undefined){
        that.trafficFlowData[+data.weekday][+data.pick_hour] = {}
      }
      that.trafficFlowData[+data.weekday][+data.pick_hour][(data.lat + ":" +data.long)] = total;
    });

    that.sentimentData = {};
    d3.csv("static/data/sentiment_number.csv", function(data){
      if(that.sentimentData[+data.day] === undefined){
        that.sentimentData[+data.day] = {};
      }
      if(that.sentimentData[+data.day][+data.hour] === undefined){
        that.sentimentData[+data.day][+data.hour] = {}
      }
      that.sentimentData[+data.day][+data.hour]["negative"] = +data.negative;
      that.sentimentData[+data.day][+data.hour]["neutral"] = +data.neutral;
      that.sentimentData[+data.day][+data.hour]["positive"] = +data.positive;
    });
  },
  mounted: function(){
    var that = this;

    var svg_criminal = d3.select("#map_svg_criminal");
    var svg_traffic = d3.select("#map_svg_traffic");

    var width = +svg_criminal.attr('width');
    var height = +svg_criminal.attr('height');
    // that.projection = d3.geoMercator()
    //                     .center([-73.94, 40.70])
    //                     .scale(50000)
    //                     .translate([width/2, height/2]);

    that.projection = d3.geoMercator()
                         .center([-73.94, 40.78])
                         .scale(130000)
                         .translate([width/2, height/2]);

    var svg_offset_criminal = that.getOffset( document.getElementById('map_criminal_col'));
    var svg_offset_traffic = that.getOffset( document.getElementById('map_traffic_col'));

    var canvasLayer_criminal = d3.select("#map_criminal_col")
      .append('canvas')
      .attr('id', 'heatmap_criminal')
      .attr('width', width)
      .attr('height', height)
      .style("position", "absolute")
      .style("top", svg_offset_criminal.top.toString() + "px")
      .style("left", svg_offset_criminal.left.toString() + "px")

    var canvasLayer_traffic = d3.select("#map_traffic_col")
      .append('canvas')
      .attr('id', 'heatmap_traffic')
      .attr('width', width)
      .attr('height', height)
      .style("position", "absolute")
      .style("top", svg_offset_traffic.top.toString() + "px")
      .style("left", svg_offset_traffic.left.toString() + "px")

    that.canvas_criminal = canvasLayer_criminal.node();
    that.canvas_traffic = canvasLayer_traffic.node();
    var context_criminal = that.canvas_criminal.getContext("2d");
    var context_traffic = that.canvas_traffic.getContext("2d");
    context_criminal.globalAlpha = 0.8;
    context_traffic.globalAlpha = 0.8;

    that.createChart("sentiment-chart");

    that.$refs.hourSlider.setIndex(12);
    that.$refs.daySlider.setIndex(1);
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
        var that = this;
        that.currHour = +that.hourSliderValue;

        this.updateCriminalDataBar();
        this.updateTrafficFlow();
        this.updateSentiment();
      }
    },
    daySliderValue: {
      handler: function(){
        var that = this;
        that.currDay = +that.dayIndexMap[that.daySliderValue];

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
    createChart(chartId) {
      var canvas = document.getElementById(chartId);
      this.sentimentDonutChart = new Chart(canvas, {
        type: this.donut_config.type,
        data: this.donut_config.data,
        options: this.donut_config.options,
      });
    },
    updateCriminalDataBar: function(){
      var that = this;
      var svg = d3.select("#map_svg_criminal")

      var heat = simpleheat(that.canvas_criminal);

      // var quantize = d3.scaleLinear()
      //   .domain([0, that.maxNbCriminal])
      //   .range([0, 80]);

      // var heatData = [];
      // for(var i = 0; i < that.precinctCenter.length; i++){
      //   var d = that.precinctCenter[i];
      //   var keyData = [];
      //   keyData.push(d[0]);
      //   keyData.push(d[1]);
      //   keyData.push(+that.criminalData[that.currDay][that.currHour][d[2]]);
      //   heatData.push(keyData);
      // }
      // heat.data(heatData);
      // heat.radius(10, 10);
      // // heat.gradient({0: '#0000ff', 0.5: '#00ff00', 1: '#ff0000'});
      // heat.max(40);
      // heat.draw(0.05);

      var keys = Object.keys(that.criminalData[that.currDay][that.currHour])

      var heatData = []
      keys.forEach(function(key){
        var lat = +key.split(":")[0];
        var long = +key.split(":")[1];
        var coord = that.projection([long, lat])
        
        var keyData = [];
        keyData.push(coord[0])
        keyData.push(coord[1])
        keyData.push(+that.criminalData[that.currDay][that.currHour][key])
        heatData.push(keyData);
      })
      heat.data(heatData);
      heat.radius(10, 10);
      // heat.gradient({0: '#0000ff', 0.5: '#00ff00', 1: '#ff0000'});
      heat.max(that.maxNbCriminal);
      heat.draw(0.05);
    },
    updateTrafficFlow: function(){
      var that = this;

      var svg = d3.select("#map_svg_traffic");

      var heat = simpleheat(that.canvas_traffic);
      var keys = Object.keys(that.trafficFlowData[that.currDay][that.currHour])
      
      // d3.selectAll("circle").remove();

      var heatData = []
      keys.forEach(function(key){
        var lat = +key.split(":")[0];
        var long = +key.split(":")[1];
        var coord = that.projection([long, lat])
        
        var keyData = [];
        keyData.push(coord[0])
        keyData.push(coord[1])
        keyData.push(+that.trafficFlowData[that.currDay][that.currHour][key])
        heatData.push(keyData);

        // Add Circle to traffic map
        // svg.append('circle')
        //     .attr('cx', coord[0])
        //     .attr('cy', coord[1])
        //     .attr('r', +that.trafficFlowData[that.currDay][that.currHour][key] / that.maxNbCriminal * 0.1);
      })
      heat.data(heatData);
      heat.radius(7, 10);
      // heat.gradient({0: '#0000ff', 0.5: '#00ff00', 1: '#ff0000'});
      heat.max(that.maxNbTraffic);
      heat.draw(0.05);
    },
    updateSentiment: function(){
      var that = this;

      that.donut_config.data.datasets[0].data = [that.sentimentData[that.currDay][that.currHour]["negative"],
                                                 that.sentimentData[that.currDay][that.currHour]["neutral"],
                                                 that.sentimentData[that.currDay][that.currHour]["positive"]];
      that.sentimentDonutChart.update();

    },
    animation: function(){
      var that = this;
      var pauseSec = 250;
      // that.animationHour(0, pauseSec);
      // that.animationDay(0, pauseSec);
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
    animationDay: function(dayIdx, pauseSec){
      var that = this;
      if(dayIdx <= 6){
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
    getOffset: function(el) {
      const rect = el.getBoundingClientRect();
      return {
        left: rect.left + window.scrollX,
        top: rect.top + window.scrollY
      };
    }
  },
}
</script>

<style>

circle{
	fill: green;
  opacity: 0.8;
  fill-opacity: .5;
}

#playBtn{
  border: 1px solid black;
  border-radius: 25px;
}

#sentiment-chart{
  position: absolute;
  left:0px;
  top: 100px;
}

// .q0 { fill:rgb(247,251,255) }
// .q1 { fill:rgb(222,235,247) }
// .q2 { fill:rgb(198,219,239) }
// .q3 { fill:rgb(158,202,225) }
// .q4 { fill:rgb(107,174,214) }
// .q5 { fill:rgb(66,146,198) }
// .q6 { fill:rgb(33,113,181) }
// .q7 { fill:rgb(8,81,156) }
// .q8 { fill:rgb(8,48,107) }
.q0 { fill:rgb(204, 204, 204) }
.q1 { fill:rgb(204, 178, 178) }
.q2 { fill:rgb(204, 153, 153) }
.q3 { fill:rgb(204, 127, 127) }
.q4 { fill:rgb(204, 102, 102) }
.q5 { fill:rgb(204, 76, 76) }
.q6 { fill:rgb(204, 51, 51) }
.q7 { fill:rgb(204, 25, 25) }
.q8 { fill:rgb(204, 0, 0) }
</style>