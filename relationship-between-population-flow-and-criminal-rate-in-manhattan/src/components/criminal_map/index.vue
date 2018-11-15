<template>
    <div class="criminalMap">
      <h1>{{title}}</h1>
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
          ref="monthSlider"
          v-model="monthSliderValue"
          v-bind="monthSliderOption"
        >
        </vue-slider>
      </div>
      <button v-on:click="animation">animation</button>
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
  name: 'criminal-map',
  data: function() {
    return {
      title: 'Criminal Map',
      criminalData: undefined,
      trafficFlowData: undefined,
      currPrecinct: undefined,
      currMonth: 1,
      currHour: 0,
      maxNbCriminal: 0,
      maxNbTraffic: 0,
      hourSliderValue: undefined,
      monthSliderValue: undefined,

      monthSliderOption:{
        width: 'auto',
        tooltip: "always",
        disable: false,
        piecewise: true,
        piecewiseLabel: true,
        startAnimation: true,
        data:[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
      },
      hourSliderOption:{
        width: 'auto',
        tooltip: "always",
        disable: false,
        piecewise: true,
        piecewiseLabel: true,
        startAnimation: true,
        data:[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
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

      if(that.criminalData[+data.month] === undefined){
        that.criminalData[+data.month] = {}
      }

      if(that.criminalData[+data.month][+data.hour] === undefined){
        that.criminalData[+data.month][+data.hour] = {}
      }
      
      if(that.criminalData[+data.month][+data.hour][+data.precinct] === undefined){
        that.criminalData[+data.month][+data.hour][+data.precinct] = {}
      }
      
      that.criminalData[+data.month][+data.hour][+data.precinct] ["totalNumber"] = +data["totalNumber"];
      that.criminalData[+data.month][+data.hour][+data.precinct] ["felony"] = +data["felony"];
      that.criminalData[+data.month][+data.hour][+data.precinct] ["misdemeanor"] = +data["misdemeanor"];
      that.criminalData[+data.month][+data.hour][+data.precinct] ["violation"] = +data["violation"];
      }
    );

    that.trafficFlowData = {};
    // d3.csv("static/data/final_table_test.csv", function(data){
    //   var total = +data.HOURLY_ENTRIES + (+data.HOURLY_EXITS);
    //   if(that.maxNbTraffic < +total){
    //     that.maxNbTraffic = +total;
    //   }

    //   if(that.trafficFlowData[+1] === undefined){
    //     that.trafficFlowData[+1] = {}
    //   }

    //   if(that.trafficFlowData[+1][+data.HOUR] === undefined){
    //     that.trafficFlowData[+1][+data.HOUR] = {}
    //   }

    //   that.trafficFlowData[+1][+data.HOUR][(data.Latitude + ":" +data.Longitude)] = total;
    // });

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
  },
  computed:{
    currentPrecinctTitle: function(){
      return "Precinct: " + this.currPrecinct;
    },
    currentPrecinctDescription: function(){
      return "Number of Crime: " + this.criminalData[this.currMonth][this.currHour][this.currPrecinct]["totalNumber"];
    },
  },
  watch: {
    hourSliderValue: {
      handler: function(){
        console.log("hour sliderValue change")
        var that = this;
        that.currHour = that.hourSliderValue;
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
          s.attr("class", precinctContext + " " + precinctSuffix + " " + quantize(that.criminalData[that.currMonth][that.currHour][+precinctNum]["totalNumber"]))
        });
        this.updateCriminalDataBar();
        this.updateTrafficFlow();
      }
    },
    monthSliderValue: {
      handler: function(){
        console.log("hour sliderValue change")
        var that = this;
        that.currMonth = that.monthSliderValue;
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
          s.attr("class", precinctContext + " " + precinctSuffix + " " + quantize(that.criminalData[that.currMonth][that.currHour][+precinctNum]["totalNumber"]))
        });
        this.updateCriminalDataBar();
        this.updateTrafficFlow();
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
      this.$refs.hourSlider.setIndex(12);
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
            return that.criminalData[that.currMonth][that.currHour][precinctNum]["totalNumber"];
          })
          .attr('width', 3)
          .attr('y', function() {
            return -that.criminalData[that.currMonth][that.currHour][precinctNum]["totalNumber"];
          })
          .attr("class", "bars")
          .style("fill", "blue")
          .style("stroke", "white")
          .style("stroke-width", 0.5)
          .style("opacity", 0.7);
      })
    },
    removeCircles: function(){
      d3.selectAll("circle")
        .remove();
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
      console.log(that.currMonth, that.currHour)
      var keys = Object.keys(that.trafficFlowData[that.currMonth][that.currHour])
      
      that.removeCircles();
      keys.forEach(function(key){
        var lat = +key.split(":")[0];
        var long = +key.split(":")[1];
        var coord = projection([long, lat])

        svg.append('circle')
            .attr('cx', coord[0])
            .attr('cy', coord[1])
            .attr('r', +that.trafficFlowData[that.currMonth][that.currHour][key] / that.maxNbCriminal * 0.1);
      })

     var test = projection([-73.94, 40.70])
      svg.append('svg:circle')
          .attr('cx', test[0])
          .attr('cy', test[1])
          .attr('r', 3);
    },
    animation: function(){
      var that = this;
      var pauseSec = 500;
      setTimeout(function(){ 
        that.$refs.hourSlider.setValue(0);
        setTimeout(function(){ 
          that.$refs.hourSlider.setValue(1);
          setTimeout(function(){ 
            that.$refs.hourSlider.setValue(2);
            setTimeout(function(){ 
              that.$refs.hourSlider.setValue(3);
              setTimeout(function(){ 
                that.$refs.hourSlider.setValue(4);
                setTimeout(function(){ 
                  that.$refs.hourSlider.setValue(5);
                  setTimeout(function(){ 
                    that.$refs.hourSlider.setValue(6);
                    setTimeout(function(){ 
                      that.$refs.hourSlider.setValue(7);
                      setTimeout(function(){ 
                        that.$refs.hourSlider.setValue(8);
                        setTimeout(function(){ 
                          that.$refs.hourSlider.setValue(9);
                          setTimeout(function(){ 
                            that.$refs.hourSlider.setValue(10);
                            setTimeout(function(){ 
                              that.$refs.hourSlider.setValue(11);
                              setTimeout(function(){ 
                                that.$refs.hourSlider.setValue(12);
                                setTimeout(function(){ 
                                  that.$refs.hourSlider.setValue(13);
                                  setTimeout(function(){ 
                                    that.$refs.hourSlider.setValue(14);
                                    setTimeout(function(){ 
                                      that.$refs.hourSlider.setValue(15);
                                      setTimeout(function(){ 
                                        that.$refs.hourSlider.setValue(16);
                                        setTimeout(function(){ 
                                          that.$refs.hourSlider.setValue(17);
                                          setTimeout(function(){ 
                                            that.$refs.hourSlider.setValue(18);
                                            setTimeout(function(){ 
                                              that.$refs.hourSlider.setValue(19);
                                              setTimeout(function(){ 
                                                that.$refs.hourSlider.setValue(20);
                                                setTimeout(function(){ 
                                                  that.$refs.hourSlider.setValue(21);
                                                  setTimeout(function(){ 
                                                    that.$refs.hourSlider.setValue(22);
                                                    setTimeout(function(){ 
                                                      that.$refs.hourSlider.setValue(23);
                                                    }, pauseSec);
                                                  }, pauseSec);
                                                }, pauseSec);
                                              }, pauseSec);
                                            }, pauseSec);
                                          }, pauseSec);
                                        }, pauseSec);
                                      }, pauseSec);
                                    }, pauseSec);
                                  }, pauseSec);
                                }, pauseSec);
                              }, pauseSec);
                            }, pauseSec);
                          }, pauseSec);
                        }, pauseSec);
                      }, pauseSec);
                    }, pauseSec);
                  }, pauseSec);
                }, pauseSec);
              }, pauseSec);
            }, pauseSec);
          }, pauseSec);
        }, pauseSec);
      }, pauseSec);
    }
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