<template>
  <div class="chart_plot">
    <h1 style="position:absolute; top:3px; left:45%; color:white">{{title}}</h1>

    <h4 style="position:absolute; top:95px; left:275px; color:black">Area</h4>
    <h4 style="position:absolute; top:95px; left:475px; color:black">Number of Residents</h4>
    <h4 style="position:absolute; top:95px; left:810px; color:black">Pearson Correlation</h4>

    <div class="container-fluid">
      <div class="row" style="padding-left:30px">
        <div class="col-md-9 cliente">
          <div class="chartHolder">
          </div>
        </div>
        
        <div class="col-md-3" style="padding-left: 40px;padding-right: 35px;">
          <div class="row cliente">
            <div class="sentimentHolder ">
              <canvas id="sentiment-chart" class="" width="310" height="310"></canvas>
            </div>
          </div>
          <div class="row  mt-4 cliente" >
            <div class="card bg-light" style="width: 315px; height:290px">
              <div class="card-header">
                {{currTitle}}
              </div>
              <div class="card-body">
                <p class="card-text">
                  {{currContext}}
                </p>
              </div>
              <div class="card-footer" style="padding:0.35rem 1.25rem;">
                <small class="text-muted">
                  <button type="button" class="btn btn-secondary " style="float:left;  border-radius:50%" v-on:click="switchToPrevPage"><font-awesome-icon icon="arrow-left" class=""/></button>

                  <center class="text-monospace" style="padding-top:10px; display:inline-block">{{currPage}} / {{totalPage}}</center>

                  <button type="button" class="btn btn-secondary " style="float:right;  border-radius:50%" v-on:click="switchToNextPage"><font-awesome-icon icon="arrow-right" class=""/></button>
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="sliderHolder my-3 cliente" style="margin-left: 15px;margin-right: 4px; padding-top:3px; padding-bottom:1px;">
        <div class="row">
          <div class="col-md-1">
              <div  style="float:right"><h5><span class="badge badge-pill badge-primary ml-4 mr-1">Time </span> </h5></div>
              <div  style="float:right"><h5> <span class="badge badge-pill badge-primary ml-4 mr-1">Day </span> </h5></div>
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
            <button id="playBtn" class="btn btn-primary  btn-lg my-1" style="float:left;" v-on:click="animation"><font-awesome-icon icon="play" class="ml-1"/></button>
          </div> 
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import vueSlider from 'vue-slider-component';
import * as d3 from 'd3';
import * as d3Legend from 'd3-svg-legend';
const chart = require("../donut_chart.js").default;

const pearsonCorrelation = require("./ pearsoncorrelation.js");

const margin = {
  top: 19.5,
  right: 19.5,
  bottom:19.5,
  left:29.5
}

const xMin = 1;
const xMax = 280000;
const yMin = 0;
const yMax = 450;
const svgWidth = 1000;
const svgHeight = 630;
const rMax = 250162;
const rMin = 1;

const manhattan_precinct = ["1", "5", "6", "7", "9", "10", "13", "14", "17", "18", "19", "20", "22", "23", "24", "25", "26", "28", "30", "32", "33", "34"];

// 0:downtown 1:midtown 2: uptown 3: uppertown   -- according to wiki(https://en.wikipedia.org/wiki/List_of_Manhattan_neighborhoods) and google map (search midtown manhattan)
const precinct_area_map = {"1": 0, "5":0, "6":0, "7":0, "9":0, 
                           "10":1, "13":1, "14":1, "17":1, "18":1, 
                           "19":2, "20":2, "22":2, "23":3, "24":2, 
                           "25":3, "26":3, "28":3, "30":3, "32":3, "33":3, "34":3}

export default {
  components: {
    vueSlider,
  },
  name: 'chart-plot-page',
  data: function() {
    return {
      title: "Chart Plot",

      // Axis property
      width: svgWidth - margin.right,
      height: svgHeight - margin.top - margin.bottom,
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
      gdots_dict: {},
      line: undefined,
      pearson_text: undefined,
      
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

      // Story
      StoryTitle: [
        "Story Telling",
        "title1",
        "title2",
        "title3",
        "title4",
        "title5"
      ],
      StoryContext: [
        "Highlight the main pattern of this map.",
        "contenxt1",
        "contenxt2",
        "contenxt3",
        "contenxt4",
        "contenxt5"
      ],
      hourList: [2, 4, 6, 8, 10],
      dayList: ["FRI", "THU", "WED", "TUE", "MON"],
      currPage: 0,
      totalPage: 5,
      currTitle: "placeholder",
      currContext: "placeholder",

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
      /// Donut chart
      donut_config: {
        type: 'doughnutLabels',
        data: {
          datasets: [{
            data: [
              1,1
            ],
            backgroundColor: [
                'rgb(75, 192, 192)',
                //'rgb(54, 162, 235)',
                'rgb(255, 99, 132)',
            ],
            label: 'Sentiment'
          }],
          labels: [
            "Positive",
            // "Neutral",
            "Negative"
          ]
        },
        options: {
          responsive: false,
          maintainAspectRatio: false,
          legend: {
            labels:{
              usePointStyle: true,
            },
            position: 'top',
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
        if(that.combine_data[+data.day][+data.hour] === undefined){
          that.combine_data[+data.day][+data.hour] = []
        }

        that.combine_data[+data.day][+data.hour].push({"precinct": +data.precinct, "criminal": total_criminal, "traffic": total_traffic, "population": +data.population, "age": +data.age, "area": precinct_area_map[data.precinct]});
      }

      count1++;

      if(count1 >= 7 * 24 * 75){
        that.$refs.hourSlider.setIndex(12);
        that.$refs.daySlider.setIndex(1);
        that.$refs.hourSlider.setIndex(0);
        that.$refs.daySlider.setIndex(0);
        that.$refs.hourSlider.setIndex(6);
        that.$refs.daySlider.setIndex(6);
      }
    });

    var count2 = 0;
    that.sentimentData = {};
    d3.csv("static/data/sentiment_number.csv", function(data){
      if(that.sentimentData[+data.day] === undefined){
        that.sentimentData[+data.day] = {};
      }
      if(that.sentimentData[+data.day][+data.hour] === undefined){
        that.sentimentData[+data.day][+data.hour] = {}
      }
      that.sentimentData[+data.day][+data.hour]["negative"] = +data.negative;
      // that.sentimentData[+data.day][+data.hour]["neutral"] = +data.neutral;
      that.sentimentData[+data.day][+data.hour]["positive"] = +data.positive;

      count2++;

      if(count2 >= 7 * 24 * 75){
        that.$refs.hourSlider.setIndex(5);
        that.$refs.daySlider.setIndex(0);
        that.$refs.hourSlider.setIndex(1);
        that.$refs.daySlider.setIndex(0);
        that.$refs.hourSlider.setIndex(6);
        that.$refs.daySlider.setIndex(6);
      }
    });
  },
  mounted: function(){
    var that = this;

    that.createChart("sentiment-chart");

    that.xScale = d3.scaleLinear().domain([xMin, xMax]).range([0, that.width]);
    that.yScale = d3.scaleLinear().domain([yMin, yMax]).range([that.height, 0]);
    that.radiusScale = d3.scaleSqrt().domain([0, rMax]).range([0, 40]);
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
      .text("# of commuters");

    svg.append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("y", 6)
      .attr("dy", ".75em")
      .attr("transform", "rotate(-90)")
      .text("# of crimes");
    
     svg.append("text")
      .attr("class", "pearson_text")
      .attr("text-anchor", "end")
      .attr("x", that.width - 105)
      .attr("y", 75)
      .text("Pearson: ")

    that.pearson_text = svg.append("text")
      .attr("class", "pearson_text")
      .attr("text-anchor", "end")
      .attr("x", that.width)
      .attr("y", 78);
    
    that.pearson_text.text("0.00");

    that.currTitle = that.StoryTitle[that.currPage];
    that.currContext = that.StoryContext[that.currPage];
  },
  methods:{
    switchToPrevPage: function(){
      if(this.currPage <= 1){
        this.currPage = this.totalPage;
      }
      else{
        this.currPage--;
      }
    },
    switchToNextPage: function(){
      if(this.currPage == this.totalPage){
        this.currPage = 1;
      }
      else{
        this.currPage++;
      }
    },
    setIdx: function(hourIdx, dayIdx){
      console.log(hourIdx, dayIdx)
      this.$refs.hourSlider.setIndex(hourIdx);
      this.$refs.daySlider.setIndex(dayIdx);
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
    leastSquares: function(xSeries, ySeries) {
      var reduceSumFunc = function(prev, cur) { return prev + cur; };
      
      var xBar = xSeries.reduce(reduceSumFunc) * 1.0 / xSeries.length;
      var yBar = ySeries.reduce(reduceSumFunc) * 1.0 / ySeries.length;
      var ssXX = xSeries.map(function(d) { return Math.pow(d - xBar, 2); })
        .reduce(reduceSumFunc);
      var ssYY = ySeries.map(function(d) { return Math.pow(d - yBar, 2); })
        .reduce(reduceSumFunc);
      var ssXY = xSeries.map(function(d, i) { return (d - xBar) * (ySeries[i] - yBar); })
        .reduce(reduceSumFunc);
      var slope = ssXY / ssXX;
      var intercept = yBar - (xBar * slope);
      var rSquare = Math.pow(ssXY, 2) / (ssXX * ssYY);
      
      return [slope, intercept, rSquare];
    },
    createChart(chartId) {
      var canvas = document.getElementById(chartId);
      this.sentimentDonutChart = new Chart(canvas, {
        type: this.donut_config.type,
        data: this.donut_config.data,
        options: this.donut_config.options,
      });
    },
    getColorData: function(age){
      age = Math.round(age);
      let type = Math.round((age - 28) / 2);
      if(type < 0){
        type = 0;
      }
      if(type > 9){
        type = 9;
      }
      return type;
    },
    isEmpty: function(obj) {
      for(var key in obj) {
          if(obj.hasOwnProperty(key))
              return false;
      }
      return true;
    },
    updateSentiment: function(){
      var that = this;

      that.donut_config.data.datasets[0].data = [that.sentimentData[that.currDay][that.currHour]["positive"],
                                                //  that.sentimentData[that.currDay][that.currHour]["neutral"],
                                                 that.sentimentData[that.currDay][that.currHour]["negative"]];
      that.sentimentDonutChart.update();

    },
    updateGraph: function(){
      var that = this;
      console.log('updategraph')

      var svg = d3.select("svg");
      svg.append("g")
        .attr("class", "legendSequential")
        .attr("transform", "translate(150,70)");

      var legendSequential = d3Legend.legendColor()
          .shapeWidth(50)
          .cells(10)
          .orient("horizontal")
          .scale(that.colorScale) 
          .labels(["Uppertown", "UpTown", "Midtown", "Downtown"]);

      svg.select(".legendSequential")
        .call(legendSequential);

      svg.append("g")
        .attr("class", "legendSize")
        .attr("transform", "translate(410, 60)");

      var legendSize = d3Legend.legendSize()
        .scale(that.radiusScale)
        .shape('circle')
        .shapePadding(15)
        .labelOffset(20)
        .orient('horizontal')
        .labels(["", "62541", "125081", "187621", "250162"]);

      svg.select(".legendSize")
        .call(legendSize);

      var svg = d3.select("svg")
                  .append("g")
                  .attr("transform", "translate(" + that.marginLeft + "," + that.marginTop + ")");

      let criminal_arr = [];
      let traffic_arr = [];
      var gdots = svg.append("g").attr("class", "dots");
      if(that.isEmpty(that.gdots_dict)){
        for(var i = 0; i < that.combine_data[that.currDay][that.currHour].length; i++){
          var val = that.combine_data[that.currDay][that.currHour][i];
          that.gdots_dict[val.precinct] = gdots.append("circle")
            .attr("class", "dot")
            .attr("id", "precinct" + val.precinct.toString())
            // .style("fill", that.colorScale(that.getColorData(val.age)))
            .style("fill", that.colorScale(val.area))
            .attr("cx", that.xScale(val.traffic))
            .attr("cy", that.yScale(val.criminal))
            .attr("r", that.radiusScale(val.population));

          that.gdots_dict[val.precinct].append("title").text("precinct_#" + val.precinct.toString());

          criminal_arr.push(val.criminal);
          traffic_arr.push(val.traffic);
        }

        var leastSquaresCoeff = that.leastSquares(traffic_arr, criminal_arr);
        var slope = leastSquaresCoeff[0];
        var intercept = leastSquaresCoeff[1];
        var rSquare = leastSquaresCoeff[2];
        var x1 = xMin;
        var x2 = xMax;
        var y1 = intercept;
        var y2 = xMax * slope + intercept;
        // if(y2 < 0){
        //   x2 = (-intercept) / slope;
        //   y2 = 0;
        // }
        that.line = svg.append("line")
          .attr("x1", that.xScale(x1))
          .attr("y1", that.yScale(y1))
          .attr("x2", that.xScale(x2))
          .attr("y2", that.yScale(y2))
          .classed("regression", true);
      }
      else{
        for(var i = 0; i < that.combine_data[that.currDay][that.currHour].length; i++){
          var val = that.combine_data[that.currDay][that.currHour][i];
          that.gdots_dict[val.precinct]
            .transition()
            .attr("cx", that.xScale(val.traffic))
            .attr("cy", that.yScale(val.criminal))

          criminal_arr.push(val.criminal);
          traffic_arr.push(val.traffic);
        }

        var leastSquaresCoeff = that.leastSquares(traffic_arr, criminal_arr);
        var slope = leastSquaresCoeff[0];
        var intercept = leastSquaresCoeff[1];
        var rSquare = leastSquaresCoeff[2];
        var x1 = xMin;
        var x2 = xMax;
        var y1 = intercept;
        var y2 = xMax * slope + intercept;
        // if(y2 < 0){
        //   x2 = (-intercept) / slope;
        //   y2 = 0;
        // }
        that.line.transition()
          .attr("x1", that.xScale(x1))
          .attr("y1", that.yScale(y1))
          .attr("x2", that.xScale(x2))
          .attr("y2", that.yScale(y2))
      }
      let rho = pearsonCorrelation.pearsonCorrelation(criminal_arr, traffic_arr);
      that.pearson_text.transition().text(rho.toFixed(2));
    }
  },
  watch: {
    currPage:{
      handler: function(){
        var that = this;
        that.setIdx(that.hourList[that.currPage], that.dayIndexMap[that.dayList[that.currPage]]);

        that.currTitle = that.StoryTitle[that.currPage];
        that.currContext = that.StoryContext[that.currPage];
      }
    },
    hourSliderValue: {
      handler: function(){
        var that = this;
        that.currHour = +that.hourSliderValue;
        that.updateGraph();
        that.updateSentiment();
      }
    },
    daySliderValue: {
      handler: function(){
        var that = this;
        that.currDay = +that.dayIndexMap[that.daySliderValue];
        that.updateGraph();
        that.updateSentiment();
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
  // stroke: #000;
  opacity:0.8;
}

.axis path, .axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.pearson_text{
  font: 500 45px "Helvetica Neue";
  fill: #ddd;
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
  border-radius: 50%;
}

.regression {
  stroke-width: 2px;
  stroke: steelblue;
  stroke-dasharray: 10,5;
}

.legendSequential{
  fill: black;
}

.legendSize{
  fill: #00BFFF;
}

.x.label{
  font: 500 20px "Helvetica Neue";
  fill: black;
}
.y.label{
  font: 500 20px "Helvetica Neue";
  fill: black;
}


.cliente {
  border: #cdcdcd medium solid;
  border-radius: 10px;
  -moz-border-radius: 10px;
  -webkit-border-radius: 10px;
}

#app{
  margin-top: 30px;
}
</style>