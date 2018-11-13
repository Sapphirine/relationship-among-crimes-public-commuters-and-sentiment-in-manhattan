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
          ref="slider"
          v-model="sliderValue"
          v-bind="vueSliderOption"
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
      precinctData: undefined,
      currPrecinct: undefined,
      currYear: undefined,
      maxNbCriminal: 0,
      sliderValue: undefined,

      vueSliderOption:{
        width: 'auto',
        tooltip: "always",
        disable: false,
        piecewise: true,
        piecewiseLabel: true,
        startAnimation: true,
        data:[2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]
      }
    }
  },
  created: function(){
    console.log("created")
    var that = this;
    that.precinctData = {2007:{}, 2008:{}, 2009:{}, 2010:{}, 2011:{}, 2012:{}, 2013:{}, 2014:{}};
    d3.csv("static/data/clean-summons-data.csv", function(data) {
      if(that.maxNbCriminal === 0){
        that.maxNbCriminal = parseInt(data["Max"]);
      }
      that.precinctData[2007][data["Precinct"]] = +data["2007"]
      that.precinctData[2008][data["Precinct"]] = +data["2008"]
      that.precinctData[2009][data["Precinct"]] = +data["2009"]
      that.precinctData[2010][data["Precinct"]] = +data["2010"]
      that.precinctData[2011][data["Precinct"]] = +data["2011"]
      that.precinctData[2012][data["Precinct"]] = +data["2012"]
      that.precinctData[2013][data["Precinct"]] = +data["2013"]
      that.precinctData[2014][data["Precinct"]] = +data["2014"]
      }
    );
  },
  computed:{
    currentPrecinctTitle: function(){
      return "Precinct: " + this.currPrecinct;
    },
    currentPrecinctDescription: function(){
      return "Number of Crime: " + this.precinctData[this.currYear][this.currPrecinct];
    },
  },
  watch: {
    sliderValue: {
      handler: function(){
        console.log("sliderValue change")
        var that = this;
        that.currYear = that.sliderValue;
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
          s.attr("class", precinctContext + " " + precinctSuffix + " " + quantize(that.precinctData[that.currYear][precinctNum]))
        });
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
      this.$refs.slider.setIndex(1);
    },
    animation: function(){
      var that = this;
      setTimeout(function(){ 
        that.$refs.slider.setValue(2007);
        setTimeout(function(){ 
          that.$refs.slider.setValue(2008);
          setTimeout(function(){ 
            that.$refs.slider.setValue(2009);
            setTimeout(function(){ 
              that.$refs.slider.setValue(2010);
              setTimeout(function(){ 
                that.$refs.slider.setValue(2011);
                setTimeout(function(){ 
                  that.$refs.slider.setValue(2012);
                  setTimeout(function(){ 
                    that.$refs.slider.setValue(2013);
                    setTimeout(function(){ 
                      that.$refs.slider.setValue(2014);
                    }, 1000);
                  }, 1000);
                }, 1000);
              }, 1000);
            }, 1000);
          }, 1000);
        }, 1000);
      }, 1000);
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