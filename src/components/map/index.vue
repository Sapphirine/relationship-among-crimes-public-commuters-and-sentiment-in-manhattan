<template>
  <div class="criminalMap">
    <div class="container">
      <h1>{{title}}</h1>
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
      <div class="sliderHolder my-2 mb-2 container">
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
          <div class="col-md-7">
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
          <div class="col-md-2">
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
import x3dom from 'x3dom';

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
      currPrecinct: undefined,
      maxNbCriminal: 0,
      scene: undefined,
      
      // Traffic Data
      trafficFlowData: undefined,
      maxNbTraffic: 0,
      canvas: undefined,

      // Sentiment Data
      senmentimentData: undefined,
      sentimentEmoji: undefined,
      sentimentEmojis: [
        "static/images/1.png",
        "static/images/2.png",
        "static/images/3.png",
        "static/images/4.png",
        "static/images/5.png",
      ],

      // Utils
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
      hourSliderOption:{
        width: 'auto',
        tooltip: "hover",
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
      if(that.trafficFlowData[+data.Month-1] === undefined){
        that.trafficFlowData[+data.Month-1] = {}
      }
      if(that.trafficFlowData[+data.Month-1][+data.HOUR_modified] === undefined){
        that.trafficFlowData[+data.Month-1][+data.HOUR_modified] = {}
      }
      that.trafficFlowData[+data.Month-1][+data.HOUR_modified][(data.Latitude + ":" +data.Longitude)] = total;
    });

    that.senmentimentData = {};
    var fakeData = {
      0:{
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
      1:{
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
  mounted: function(){
    var that = this;

    var svg_offset = that.getOffset( document.getElementById('map_svg'));

    var svg = d3.select(".mapHolder")
                .select("svg");
    var width = +svg.attr('width');
    var height = +svg.attr('height');
    // that.projection = d3.geoMercator()
    //                     .center([-73.94, 40.70])
    //                     .scale(50000)
    //                     .translate([width/2, height/2]);

    that.projection = d3.geoMercator()
                         .center([-73.94, 40.73])
                         .scale(80000)
                         .translate([width/2, height/2]);

    var canvasLayer = d3.select("#manhattan_map")
                        .append('canvas')
                        .attr('id', 'heatmap')
                        .attr('width', width)
                        .attr('height', height)
                        .style("position", "absolute")
                        .style("top", svg_offset.top.toString() + "px")
                        .style("left", svg_offset.left.toString() + "px")

    that.canvas = canvasLayer.node();
    var context = that.canvas.getContext("2d");
    context.globalAlpha = 0.7;

    d3.select("svg")
      .append("g")
      .attr("transform", function(d) {
        return "translate(" + "0" + "," + "0" + ")";
      })
      .append("svg:image")
      .attr("width", 200)
      .attr("height", 200)
      .attr("xlink:href", that.sentimentEmojis[2])
      .attr("alt", "img")

    var x3dCanvas = d3.select("#manhattan_map")
                      .append("x3d")
                      .attr("id", "x3dcanvas")
                      .attr( "height", height.toString()+"px")
                      .attr( "width", width.toString()+"px")
                      .style("position", "absolute")
                      .style("top", svg_offset.top.toString() + "px")
                      .style("left", svg_offset.left.toString() + "px")
    that.scene = x3dCanvas.append("scene");
    that.scene.append("viewpoint")
          .attr( "centerOfRotation", "3.75 0 10")
          .attr( "position", "13.742265188709691 -27.453522975182366 16.816062840792625" )
          .attr( "orientation", "0.962043810961999 0.1696342804961945 0.21376603254551874 1.379433089729343" );

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
        var that = this;
        that.currDay = +that.dayIndexMap[that.daySliderValue];
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
                  .select("svg")

      var bars = svg.selectAll(".bars");

      bars.each(function(){
        var bar = d3.select(this);
        var precinctNum = bar.attr("class").split(" ")[1];

        bar.select("rect")
          .attr('height', function() {
            return that.criminalData[that.currDay][that.currHour][precinctNum];
          })
          .attr('width', 10)
          .attr('y', function() {
            return -that.criminalData[that.currDay][that.currHour][precinctNum];
          })
          .attr("class", "bars")
          .style("fill", "Coral")
          .style("stroke", "white")
          .style("stroke-width", 1)
          .style("opacity", 0.8);
      })
    },
    updateTrafficFlow: function(){
      var that = this;

      var svg = d3.select(".mapHolder")
                  .select("svg");

      var heat = simpleheat(that.canvas);
      var keys = Object.keys(that.trafficFlowData[that.currDay][that.currHour])

      d3.selectAll("circle")
        .remove();

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

        // svg.append('circle')
        //     .attr('cx', coord[0])
        //     .attr('cy', coord[1])
        //     .attr('r', +that.trafficFlowData[that.currDay][that.currHour][key] / that.maxNbCriminal * 0.1);
      })
      heat.data(heatData);
      // set point radius and blur radius (25 and 15 by default)
      heat.radius(10, 10);
      // optionally customize gradient colors, e.g. below
      // (would be nicer if d3 color scale worked here)
      // heat.gradient({0: '#0000ff', 0.5: '#00ff00', 1: '#ff0000'});

      // set maximum for domain
      heat.max(that.maxNbTraffic / 2);
      // draw into canvas, with minimum opacity threshold
      heat.draw(0.05);
    },
    updateSentiment: function(){
      var that = this;
      var sentimentValue =  that.senmentimentData[that.currDay][that.currHour]["Sentiment"]


      if(sentimentValue >= -1.0 && sentimentValue < -0.75){
        d3.select("image").attr("xlink:href", that.sentimentEmojis[4])
      }
      else if(sentimentValue >= -0.75 && sentimentValue < -0.25){
        d3.select("image").attr("xlink:href", that.sentimentEmojis[3])
      }
      else if(sentimentValue >= -0.25 && sentimentValue < 0.25){
        d3.select("image").attr("xlink:href", that.sentimentEmojis[2])
      }
      else if(sentimentValue >= 0.25 && sentimentValue < 0.75){
        d3.select("image").attr("xlink:href", that.sentimentEmojis[1])
      }
      else if(sentimentValue >= 0.75 && sentimentValue < 1.0){
        d3.select("image").attr("xlink:href", that.sentimentEmojis[0])
      }
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