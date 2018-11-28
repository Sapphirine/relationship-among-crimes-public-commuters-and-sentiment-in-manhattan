<template>
    <div class="chart_plot">
      <h1 style="position:absolute; top:3px; left:45%; color:white">{{title}}</h1>
      <div class="chartHolder">
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
</template>

<script>
import vueSlider from 'vue-slider-component';
import * as d3 from 'd3';
const chart = require("../donut_chart.js").default;

const margin = {
  top: 19.5,
  right: 19.5,
  bottom:19.5,
  left:39.5
}

export default {
  components: {
    vueSlider,
  },
  name: 'chart-plot-page',
  data: function() {
    return {
      title: "Chart Plot",

      // Axis property
      width: 960 - margin.right,
      height: 500 - margin.top - margin.bottom,
      marginTop: margin.top,
      marginBottom: margin.bottom,
      marginLeft: margin.left,
      marginRight: margin.right,

      xScale: undefined,
      yScale: undefined,
      radiusScale: undefined,
      colorScale: undefined,

      // Show properties
      label: undefined,
      dayLabel: undefined,
      hourLabel: undefined,
      dot: undefined,
      
      // Commom
      currDay: 2,
      currHour: 1,

      // Criminal and traffic data
      combine_data: undefined,
      maxNbCriminal: 0,
      maxNbTraffic: 0,

      // Sentiment Data
      sentimentData: undefined,
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

    that.combine_data = {};
    d3.csv("static/data/combine_precinct.csv", function(data) {
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
      if(that.combine_data[+data.day][+data.hour] === undefined){
        that.combine_data[+data.day][+data.hour] = []
      }

      that.combine_data[+data.day][+data.hour].push({"precinct": +data.precinct, "criminal": total_criminal, "traffic": total_traffic});
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

    that.xScale = d3.scaleLinear().domain([0, 250000]).range([0, that.width]);
    that.yScale = d3.scaleLinear().domain([0, 500]).range([that.height, 0]);
    that.radiusScale = d3.scaleSqrt().domain([0, 5e8]).range([0, 40]);
    that.colorScale = d3.scaleOrdinal(d3.schemeCategory10);

    var xAxis = d3.axisBottom().scale(that.xScale);
    var yAxis = d3.axisLeft().scale(that.yScale);

    var svg = d3.select(".chartHolder")
                .append("svg")
                .attr("width", that.width + that.marginLeft + that.marginRight)
                .attr("height", that.height + that.marginTop + that.marginBottom);
    svg = d3.select("svg")
            .append("g")
            .attr("transform", "translate(" + that.marginLeft + "," + that.marginTop + ")");

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + that.height + ")")
      .call(xAxis);

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

    svg.append("text")
      .attr("class", "x label")
      .attr("text-anchor", "end")
      .attr("x", that.width)
      .attr("y", that.height - 6)
      .text("traffic flow");

    svg.append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("y", 6)
      .attr("dy", ".75em")
      .attr("transform", "rotate(-90)")
      .text("number of crime");
    
    console.log("mounted!")
  },
  methods:{
    animation: function(){
      var that = this;
      var pauseSec = 250;
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
    getXData: function(d){
      return d.traffic;
    },
    getYData: function(d){
      return d.criminal;
    },
    getRadiusData: function(d){
      return 2e6
      // return d.population;
    },
    getColorData: function(d){
      return 5;
      // return d.region;
    },
    sortASC: function(a, b){
      return this.getRadiusData(b) - this.getRadiusData(a);
    },
    sortDESC: function(a, b){
      return this.getRadiusData(a) - this.getRadiusData(b);
    },
    updateGraph: function(){
      var that = this;
      console.log('updategraph')
      var svg = d3.select("svg")
                  .append("g")
                  .attr("transform", "translate(" + that.marginLeft + "," + that.marginTop + ")");
      
      //d3.selectAll(".dots").remove();
      
      if(that.dot === undefined){
        that.dot = svg.append("g")
          .attr("class", "dots")
          .selectAll(".dot")
          .data(that.combine_data[that.currDay][that.currHour])
          .enter()
          .append("circle")
          .attr("class", "dot")
          .attr("id", function(d) { 
            return d.precinct; 
          })
          .style("fill", function(d) { return that.colorScale(that.getColorData(d)); })
          .attr("cx", function(d) { 
            return that.xScale(that.getXData(d)); })
          .attr("cy", function(d) { return that.yScale(that.getYData(d)); })
          .attr("r", function(d) { return that.radiusScale(that.getRadiusData(d))})
          .append("title").text(function(d) { return d.precinct; });
      }
      else{
         d3.selectAll(".circle")
          .data(that.combine_data[that.currDay][that.currHour])
          .transition()
          .attr("cx", function(d){
            return that.xScale(that.getXData(d));
          })
          .attr("cy", function(d){
            return that.yScale(that.getYData(d));
          })
          .attr("r", function(d){
            return that.radiusScale(that.getRadiusData(d));
          });
      }
    }
  },
  watch: {
    hourSliderValue: {
      handler: function(){
        var that = this;
        that.currHour = +that.hourSliderValue;
        this.updateGraph();
      }
    },
    daySliderValue: {
      handler: function(){
        var that = this;
        that.currDay = +that.dayIndexMap[that.daySliderValue];
        this.updateGraph();
      }
    }
  },
}
</script>

<style>

text {
  font: 10px sans-serif;
}

.dot {
  stroke: #000;
}

.axis path, .axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.label {
  fill: #777;
}
.day.label {
  font: 500 146px "Helvetica Neue";
  fill: #ddd;
}
.hour.label {
  font: 500 146px "Helvetica Neue";
  fill: #ddd;
}

.day.label.active {
  fill: #aaa;
}
.hour.label.active {
  fill: #aaa;
}

.overlay {
  fill: none;
  pointer-events: all;
  cursor: ew-resize;
}

path {
  pointer-events: all;
  // fill: none;
  stroke: #666;
  stroke-opacity: 0.2;
}

#playBtn{
  border: 1px solid black;
  border-radius: 25px;
}
</style>