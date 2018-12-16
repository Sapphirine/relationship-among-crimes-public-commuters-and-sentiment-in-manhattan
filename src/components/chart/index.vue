<template>
  <div class="chart_plot">
    <h1 style="position:absolute; top:3px;left: 50%;-webkit-transform: translateX(-50%);transform: translateX(-50%); color:white">{{title}}</h1>

    <div class="container-fluid">
      <div class="row " style="padding-left:30px">
        <div class="col-md-*">
          <div class="row">
            <div class="chartHolder cliente">
            </div>
          </div>
          <div class = "row my-3">
            <div class="col-md-12 cliente">
              <div class="row ">
                <div class="col-md-1">
                    <div  style=""><h4><span class="badge badge-pill badge-primary">Time </span> </h4></div>
                    <div  style=""><h4> <span class="badge badge-pill badge-primary">Day </span> </h4></div>
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
                  <div id="playAndPauseBtnDiv">
                    <button id="playBtn" :class="[isPlay ? 'd-none' : '', 'btn', 'btn-primary',  'btn-lg']" v-on:click="playOrPauseAnimation(true)">
                      <div ><font-awesome-icon icon="play" class=""/></div>
                    </button>
                    <button id="pauseBtn" :class="[isPlay ? '' : 'd-none' , 'btn', 'btn-primary',  'btn-lg']" v-on:click="playOrPauseAnimation(false)">
                      <div ><font-awesome-icon icon="pause" class=""/></div>
                    </button>
                  </div>
                </div> 
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-3" style="padding-left: 60px;padding-right: 35px;">
          <div class="row cliente ">
            <div class="sentimentHolder" style="height:300px;margin: 0px auto;">
              <canvas id="sentiment-chart"></canvas>
            </div>
          </div>
          <div class="row  mt-4 cliente" style="height: calc(100% - (300px + 45px); ">
            <div class="card bg-light ">
              <div class="card-header" style="max-height: calc(100% - 45px);padding-bottom: 8px;padding-top: 8px;">
                {{currTitle}}
              </div>
              <div class="card-body" id="storyContextCardBody">
                <p class="card-text" style="height:100%">
                  <div class="text-center">
                    {{currContext}}
                  </div>
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
    </div>
  </div>
</template>

<script>
import vueSlider from 'vue-slider-component';
import * as d3 from 'd3';
import * as d3Legend from 'd3-svg-legend';
const chart = require("../donut_chart.js").default;
const polygonCenter = require('geojson-polygon-center');
const topojson = require('topojson');
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

const downtown = ["1", "5", "6", "7", "9"];
const midtown = ["10", "13", "14", "17", "18"];
const uptown = ["19", "20", "22", "24"];
const uppertown = ["23", "25", "26", "28", "30", "32", "33", "34"];
const color_arr = ["rgb(214, 39, 40)", "rgb(44, 160, 44)", "rgb(31, 119, 180)", "rgb(255, 127, 14)"];

const legend_x = [100, 100, 100, 100];
const legend_y = [20, 45, 70, 95];
const legend_text = ["Uppertown", "Uptown", "Midtown", "Downtown"];
const legend_color = ["rgb(31, 119, 180)", "rgb(255, 127, 14)", "rgb(44, 160, 44)", "rgb(214, 39, 40)"];


export default {
  components: {
    vueSlider,
  },
  name: 'bubble-chart-page',
  data: function() {
    return {
      title: "Bubble Chart",

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
      mapIsReady: false,

      curr_play_hour: 0,
      curr_play_day: 0,
      isPlay: false,

      // Criminal and traffic data
      combine_data: undefined,
      maxNbCriminal: 0,
      maxNbTraffic: 0,
      data1Ready: false,

      // Sentiment Data
      sentimentData: undefined,
      sentimentDonutChart: undefined,
      data2Ready: false,

      // Story
      StoryTitle: [
        "Plot of Crime and Population",
        "Random Events",
        "Risky Night Shift",
        "Scattered Cloud",
        "Weekend Safety",
      ],
      StoryContext: [
        "This visualizationis the bubble plot of number of crimes and number public commuters, the size of bubble denotes the number of residents, and color of bubbles represents the area. We measure the correlation using pearson algo.",

        "The time that crimes happen in a random chance. The purposeless crimes are accompanied with mass communications and less obvious motive baffles investigators. However, the crimes can have more effects at the time lacks the clear clarification of sentiments.",

        "With highest Pearson correlation with value of 0.92 between the public commuters and crime, indicates that when there is a shift, there may be a crime happens. People are in negative mood, both make sense for the victims and offenders.",

        "Happy weekend is coming, everybody is exciting to move around the city. The population of public commuters arrives at the peak. It seems that there is no body cares too much about safety.",

        "Relaxing time with high public commuters.  A lot of people come to crowd in the downtown. And there is also a risk of unexpected dangers happens Be careful! When you have fun, the criminals may also have fun.",
      ],
      hourList: [2, 22, 4, 15, 12],
      dayList: ["FRI", "TUE", "THU", "FRI", "SAT"],
      currPage: 0,
      totalPage: 4,
      currTitle: "placeholder",
      currContext: "placeholder",

      // Utils
      /// Day slider
      dayIndexMap:{"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6},
      hourSliderValue: 2,
      daySliderValue: 1,
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
                'rgb(255, 99, 132)',
            ],
            label: 'Sentiment'
          }],
          labels: [
            "Positive",
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
      if(count1 >= 7 * 24 * 76){
        that.data1Ready = true;
        that.onDataReady();
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
      that.sentimentData[+data.day][+data.hour]["positive"] = +data.positive;

      count2++;
      if(count2 >= 7 * 24){
        that.data2Ready = true;
        that.onDataReady();
      }
    });
  },
  mounted: function(){
    var that = this;

    that.createChart("sentiment-chart");

    that.xScale = d3.scaleLinear().domain([xMin, xMax]).range([0, that.width]);
    that.yScale = d3.scaleLinear().domain([yMin, yMax]).range([that.height, 0]);
    that.radiusScale = d3.scaleSqrt().domain([0, rMax]).range([0, 40]);
    that.colorScale = d3.scaleOrdinal()
        .domain([0, 1, 2, 3])
        .range([color_arr[0], color_arr[1], color_arr[3], color_arr[2]]);

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
      .text("Number of commuters");

    svg.append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("y", 6)
      .attr("dy", ".75em")
      .attr("transform", "rotate(-90)")
      .text("Number of crimes");
    
     svg.append("text")
      .attr("class", "desc_text")
      .attr("text-anchor", "end")
      .attr("x", 240)
      .attr("y", 10)
      .text("Geo Location")

     svg.append("text")
      .attr("class", "desc_text")
      .attr("text-anchor", "end")
      .attr("x", 600)
      .attr("y", 10)
      .text("Number of Residents")

     svg.append("text")
      .attr("class", "desc_text")
      .attr("text-anchor", "end")
      .attr("x", that.width - 60)
      .attr("y", 10)
      .text("Linear Correlation")

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


    for(var i = 0; i < 4; i++){
      svg.append('rect')
      .attr('x', legend_x[i])
      .attr('y', legend_y[i])
      .attr('width', 50)
      .attr('height', 20)
      .style('fill', legend_color[i])
      .style('stroke', 'black')
      .style('stroke-width', '.3px')
      .style('opacity', '0.8');

      svg.append('text')
      .attr('x', legend_x[i] + 60)
      .attr('y', legend_y[i] + 15)
      .text(legend_text[i])
     }

    svg.append("g")
      .attr("class", "legendSize")
      .attr("transform", "translate(380, 40)");

    var legendSize = d3Legend.legendSize()
      .scale(that.radiusScale)
      .shape('circle')
      .shapePadding(15)
      .labelOffset(20)
      .orient('horizontal')
      .labels(["", "50000", "100000", "150000", "200000"]);

    svg.select(".legendSize")
      .call(legendSize);

    const projection = d3.geoMercator()
                         .center([-73.9735, 40.78])
                         .scale(40000)
                         .translate([that.width/2, that.height/2]);
    var path = d3.geoPath().projection(projection);

    d3.json("static/data/police_precincts.geojson")
      .then(function(geoJson) {
        svg.append('g')
          .attr("class", "test")
          .attr("transform", "translate(-250,-220)")
          .selectAll('.precinct')
          .data(function(){
            var features = geoJson.features;
            var resFeatures = [];
            for(var i = 0; i < features.length; i++){
              if(manhattan_precinct.includes(features[i].properties.Precinct.toString()) == true){
                resFeatures.push(features[i]);
              }
            }
            return resFeatures;
          })
          .enter()
          .append("path")
          .attr("class", "precinct")
          .attr("class", function(d){
            return "nb" + d.properties.Precinct;
          })
          .attr("d", path)
          .classed("precinct", true)
          .style("fill", function(d){
            let curr_precinct = d.properties.Precinct.toString();
            let color = undefined;
            if(downtown.includes(curr_precinct)){
              color = color_arr[0];
            }
            else if(midtown.includes(curr_precinct)){
              color = color_arr[1];
            }
            else if(uppertown.includes(curr_precinct)){
              color = color_arr[2];
            }
            else{
              color = color_arr[3];
            }
            return color;
          })
          .style("opacity", 0.8);

        that.mapIsReady = true;;
        that.onDataReady();
      });

    that.pearson_text.text("0.00");

    that.currTitle = that.StoryTitle[that.currPage];
    that.currContext = that.StoryContext[that.currPage];
    this.$refs.hourSlider.setIndex(12);
    this.$refs.daySlider.setIndex(3);
  },
  methods:{
    onMapIsReady: function(signal){
      this.mapIsReady = true;
      this.onDataReady();
    },
    onDataReady: function(){
      if(this.data1Ready == true && this.data2Ready == true && this.mapIsReady == true){
        this.$refs.hourSlider.setIndex(0);
        this.$refs.daySlider.setIndex(0);
      }
    },
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
      this.$refs.hourSlider.setIndex(hourIdx);
      this.$refs.daySlider.setIndex(dayIdx);
    },
    animation: function(){
      var that = this;
      var pauseSec = 300;

      if(that.isPlay == true){
        if(that.curr_play_hour < 23){
          that.curr_play_hour += 1;
        }
        else if(that.curr_play_hour == 23 && that.curr_play_day < 6){
          that.curr_play_hour = 0;
          that.curr_play_day += 1;
        }
        else{
          that.curr_play_hour = 0;
          that.curr_play_day = 0;
          that.isPlay = false;
        }
        that.$refs.hourSlider.setIndex(that.curr_play_hour);
        that.$refs.daySlider.setIndex(that.curr_play_day);
        setTimeout(that.animation, pauseSec);
      }
    },
    playOrPauseAnimation: function(is_play){
      this.isPlay = is_play;

      if(this.isPlay == true){
        this.animation();
      }
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
      canvas.style.width='100%';
      canvas.style.height='100%';
      canvas.width  = canvas.offsetWidth;
      canvas.height  = canvas.offsetHeight;
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
                                                 that.sentimentData[that.currDay][that.currHour]["negative"]];
      that.sentimentDonutChart.update();

    },
    updateGraph: function(){
      var that = this;

      var svg = d3.select("svg");
      let criminal_arr = [];
      let traffic_arr = [];

      if(that.isEmpty(that.gdots_dict)){
        var svg = d3.select("svg")
                    .append("g")
                    .attr("transform", "translate(" + that.marginLeft + "," + that.marginTop + ")");
        var gdots = svg.append("g").attr("class", "dots");
        for(var i = 0; i < that.combine_data[that.currDay][that.currHour].length; i++){
          var val = that.combine_data[that.currDay][that.currHour][i];
          that.gdots_dict[val.precinct] = gdots.append("circle")
            .attr("class", "dot")
            .attr("id", "precinct" + val.precinct.toString())
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
    currPage: function(){
        var that = this;
        that.setIdx(that.hourList[that.currPage], that.dayIndexMap[that.dayList[that.currPage]]);

        that.currTitle = that.StoryTitle[that.currPage];
        that.currContext = that.StoryContext[that.currPage];
    },
    hourSliderValue:function(){
        var that = this;
        that.currHour = +that.hourSliderValue;
        that.updateGraph();
        that.updateSentiment();
    },
    daySliderValue: function(){
        var that = this;
        that.currDay = +that.dayIndexMap[that.daySliderValue];
        that.updateGraph();
        that.updateSentiment();
    },
  },
}
</script>

<style>

text {
  font: 10px sans-serif;
}

.dot {
  opacity:0.8;
}

.axis path, .axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.pearson_text{
  font: 500 45px "Helvetica Neue";
  fill: #FF5733;
}

.desc_text{
  font: 500 20px "Helvetica Neue";
  fill: black;
}

.overlay {
  fill: none;
  pointer-events: all;
  cursor: ew-resize;
}

path {
  pointer-events: all;
  stroke: #666;
  stroke-opacity: 0.2;
}

#playBtn,#pauseBtn{
  border: 1px solid black;
  border-radius: 50%;
}
#playAndPauseBtnDiv{
  height:100%;
  display: flex;
  align-items: center;
  justify-content: center
}

.regression {
  stroke-width: 2px;
  stroke: steelblue;
  stroke-dasharray: 10,5;
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


#storyContextCardBody{
  padding: 0px 0px 0px 0px;
}

#storyContextTextArea{
  resize: none;
  height:100%;
  padding: 1px 1px 1px 1px;
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

.legendGeographic rect{
  opacity: 0.8;
}

canvas
{
    display: block;
    margin: 0 auto;
}
</style>