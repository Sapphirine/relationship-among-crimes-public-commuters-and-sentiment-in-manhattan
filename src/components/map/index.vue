<template>
  <div class="criminalMap">

    <h1 style="position:absolute; top:3px;left: 50%;-webkit-transform: translateX(-50%);transform: translateX(-50%); color:white">{{title}}</h1>

    <div class="container-fluid">
      <div class="row">
        <div class="mapHolder" style="padding-left:46px">
          <ManhattanAndNeighborMap
            @precinctSelected="onPrecinctSelected"
            @precinctDeselected="onPrecinctDeselected"
            @mapIsReady="onMapIsReady"
          />
          <div class="tooltipHolder">
            <Tooltip
              v-if="currPrecinct"
              :title="currentPrecinctTitle"
              :description="currentPrecinctDescription"
            />
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
          <div class="row  my-4 cliente" style="height: calc(100% - (300px + 45px); ">
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
import simpleheat from 'simpleheat';
// import Chart from 'chart.js';

const chart = require("../donut_chart.js").default;
const manhattanAndNeighborMap = require("./manhattan_and_neighbor_map.vue").default;
const tooltip = require("./tooltip.vue").default;

export default {
  components: {
    ManhattanAndNeighborMap: manhattanAndNeighborMap,
    Tooltip: tooltip,
    vueSlider,
  },
  name: 'heatmap-chart-page',
  data: function() {
    return {
      title: 'Heatmap Chart',

      // Commom
      projection: undefined,
      currDay: 2,
      currHour: 1,

      curr_play_hour: 0,
      curr_play_day: 0,
      isPlay: false,

      // Criminal Data
      criminalData: undefined,
      precinctCenter: undefined,
      currPrecinct: undefined,
      maxNbCriminal: 0,
      data1Ready: false,
      
      // Traffic Data
      trafficFlowData: undefined,
      maxNbTraffic: 0,
      canvas_criminal: undefined,
      canvas_traffic: undefined,
      data2Ready: false,

      // Sentiment Data
      sentimentData: undefined,
      sentimentDonutChart: undefined,
      data3Ready: false,

      // Story
      StoryTitle: [
        "Heatmap of Crime and Population",
        "Late Afternoon Malaise",
        "Blue Wednesday",
        "Morning Depression",
        "Happy Weekend",
        "Rock the Night",
        "Crime Time",
        "Peaceful Sunday Morning",
        "Nightmare",
      ],
      StoryContext: [
        "The heapmaps show dynamic crimes and commuters of Manhattan aggregated by precinct. Twitter roughly shows sentiment of people hour-by-hour in an average week.",

        "As people are working, with low commute in the city, they have a low mood around  65% of them feel upset. The criminals focusing on the Washington Square indicates that mostly, the  target of criminal is the tourist.",

        "Context: the commute and the crime happens around the mid town, where is the major work place in the city. It is the most difficult time in the whole week with highest negative percentage. Yes, nobody likes working.",

        "With less crime and traffic, only a sharp increase of negative mood in the early morning of Thursday. Circadian rhythms disruption is often the main causes of morning depression.",

        "Finally struggle to end the working. It is time to have fun! So people move around the city, especially to the hell’s kitchen to find delicious food. Everybody is delighted. What’s about the job? Forget it! It’s time to drink!",

        "People gather around the soho and little Italy neighborhood, trying to have some fun together.  The highest positive sentiment ratio, nearly 76%, with little crime.",

        "The time with the Highest crime heat, mainly around mid town( 34th pen station— time square). And people seem go around the penne station with a happy mood. Maybe they are too happy to remember the safety.",

        "No crime, no busy transportation, everything looks good. And people are all in the beautiful sleeping and relaxing style.",

        "There is no crime, no transportation around the city. But people feel sad that the weekend is ending and they have to start work again. What a long week!"
      ],
      hourList: [0, 16, 14, 5, 19, 1, 20, 6, 23],
      dayList: ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SAT", "SUN", "SUN"],
      currPage: 0,
      totalPage: 8,
      currTitle: "placeholder",
      currContext: "placeholder",

      // Utils
      /// Day slider
      dayIndexMap:{"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4, "SAT": 5, "SUN": 6},
      hourSliderValue: 1,
      daySliderValue: 2,
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

    var count1 = 0;
    that.criminalData = {};
    d3.csv("static/data/map_plot_criminal_lat_long.csv",
    // d3.csv("static/data/criminal_lat_long_01_clean.csv", 
    function(data) {
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
    
      count1++;

      if(count1 >=  764323){
        that.data1Ready = true;
        that.onDataReady();
      }
    });

    var count2 = 0;
    that.trafficFlowData = {};
    d3.csv("static/data/map_plot_commuter_lat_long.csv", 
    // d3.csv("static/data/taxi_sort_01_clean.csv",
    function(data){ 
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

      count2++;
      if(count2 >=  1497702){
        that.data2Ready = true;
        that.onDataReady();
      }
    });

    var count3 = 0;
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

      count3++;

      if(count3 >=  7*24){
        that.data3Ready = true;
        that.onDataReady();
      }
    });

    // that.$refs.hourSlider.setIndex(12);
    // that.$refs.daySlider.setIndex(3);
  },
  mounted: function(){
    var that = this;

    that.createChart("sentiment-chart");

    var svg_criminal = d3.select("#map_svg_criminal");
    var svg_traffic = d3.select("#map_svg_traffic");

    var width = +svg_criminal.attr('width');
    var height = +svg_criminal.attr('height');

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
      // .style("top", svg_offset_criminal.top.toString() + "px")
      .style("left", svg_offset_criminal.left.toString() + "px")

    var canvasLayer_traffic = d3.select("#map_traffic_col")
      .append('canvas')
      .attr('id', 'heatmap_traffic')
      .attr('width', width)
      .attr('height', height)
      .style("position", "absolute")
      // .style("top", svg_offset_traffic.top.toString() + "px")
      .style("left", svg_offset_traffic.left.toString() + "px")

    that.canvas_criminal = canvasLayer_criminal.node();
    that.canvas_traffic = canvasLayer_traffic.node();
    var context_criminal = that.canvas_criminal.getContext("2d");
    var context_traffic = that.canvas_traffic.getContext("2d");
    context_criminal.globalAlpha = 0.8;
    context_traffic.globalAlpha = 0.8;

    that.currTitle = that.StoryTitle[that.currPage];
    that.currContext = that.StoryContext[that.currPage];
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
    currPage:function(){
      var that = this;
      that.setIdx(that.hourList[that.currPage], that.dayIndexMap[that.dayList[that.currPage]]);

      that.currTitle = that.StoryTitle[that.currPage];
      that.currContext = that.StoryContext[that.currPage];
    },
    hourSliderValue: function(){
      var that = this;
      that.currHour = +that.hourSliderValue;

      this.updateCriminalDataBar();
      this.updateTrafficFlow();
      this.updateSentiment();
    },
    daySliderValue: function(){
      var that = this;
      that.currDay = +that.dayIndexMap[that.daySliderValue];

      this.updateCriminalDataBar();
      this.updateTrafficFlow();
      this.updateSentiment();
    },
  },
  methods: {
    onDataReady: function(){
      if(this.data1Ready == true && this.data2Ready == true && this.data3Ready == true){
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
    onPrecinctSelected: function(precinctIdx) {
      this.currPrecinct = precinctIdx;
    },
    onPrecinctDeselected: function(stateCode) {
      this.currPrecinct = undefined;
    },
    onMapIsReady: function(signal){
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
    updateCriminalDataBar: function(){
      var that = this;
      var svg = d3.select("#map_svg_criminal")

      var heat = simpleheat(that.canvas_criminal);

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
      heat.max(that.maxNbCriminal*0.95);
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

      that.donut_config.data.datasets[0].data = [that.sentimentData[that.currDay][that.currHour]["positive"],
                                                //  that.sentimentData[that.currDay][that.currHour]["neutral"],
                                                 that.sentimentData[that.currDay][that.currHour]["negative"]];
      that.sentimentDonutChart.update();

    },
    animation: function(){
      var that = this;
      var pauseSec = 250;

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

#criminal_map{
  position: absolute;
  left: 175px;
  top: 70px;
}

#traffic_map{
  position: absolute;
  left: 700px;
  top: 70px;
}

#sentiment_chart{
  position: absolute;
  left: 1200px;
  top: 70px;
}

#storyContextCardBody{
  padding: 0px 0px 0px 0px;
}

#storyContextTextArea{
  resize: none;
  height: 159px;
  width: 308px;
  padding: 1px 1px 1px 1px;
}

.q0 { fill:rgb(204, 204, 204) }
.q1 { fill:rgb(204, 178, 178) }
.q2 { fill:rgb(204, 153, 153) }
.q3 { fill:rgb(204, 127, 127) }
.q4 { fill:rgb(204, 102, 102) }
.q5 { fill:rgb(204, 76, 76) }
.q6 { fill:rgb(204, 51, 51) }
.q7 { fill:rgb(204, 25, 25) }
.q8 { fill:rgb(204, 0, 0) }


#app{
  margin-top: 30px;
}

.cliente {
  border: #cdcdcd medium solid;
  border-radius: 10px;
  -moz-border-radius: 10px;
  -webkit-border-radius: 10px;
}
</style>