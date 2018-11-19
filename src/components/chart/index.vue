<template>
    <div class="chart_plot">
      <h1>{{title}}</h1>
      <div class="chartHolder">
      </div>
      {{currYear}}
      <button v-on:click="increase"> test </button>
    </div>
</template>

<script>
import vueSlider from 'vue-slider-component';
import * as d3 from 'd3';

const margin = {
        top: 19.5,
        right: 19.5,
        bottom:19.5,
        left:39.5
      }

export default {
  name: 'chart-plot-page',
  data: function() {
    return {
      currYear: undefined,
      title: "Chart Plot",
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
      
      bisector: undefined,
      label: undefined,

      nationData: undefined,
      dot: undefined,
    }
  },
  mounted: function(){
    var that = this;

    that.xScale = d3.scaleLog().domain([300, 1e5]).range([0, that.width]);
    that.yScale = d3.scaleLinear().domain([10, 85]).range([that.height, 0]);
    that.radiusScale = d3.scaleSqrt().domain([0, 5e8]).range([0, 40]);
    that.colorScale = d3.scaleOrdinal(d3.schemeCategory10);

    var xAxis = d3.axisBottom().scale(that.xScale).ticks(12, d3.format(",d"));
    var yAxis = d3.axisLeft().scale(that.yScale);

    var svg = d3.select(".chartHolder")
                .append("svg")
                .attr("width", that.width + that.marginLeft + that.marginRight)
                .attr("height", that.height + that.marginTop + that.marginBottom + 130);
    svg = d3.select("svg")
            .append("g")
            .attr("transform", "translate(" + that.marginLeft + "," + that.marginTop + ")");

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + that.height + ")")
      .call(xAxis);

    // Add the y-axis.
    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

    // Add an x-axis label.
    svg.append("text")
      .attr("class", "x label")
      .attr("text-anchor", "end")
      .attr("x", that.width)
      .attr("y", that.height - 6)
      .text("income per capita, inflation-adjusted (dollars)");

    // Add a y-axis label.
    svg.append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("y", 6)
      .attr("dy", ".75em")
      .attr("transform", "rotate(-90)")
      .text("life expectancy (years)");

    // Add the year label; the value is set on transition.
    that.label = svg.append("text")
      .attr("class", "year label")
      .attr("text-anchor", "end")
      .attr("y", that.height + 130)
      .attr("x", that.width)
      .text(1800);

    d3.json("static/demo_data/data/nations.json").then(function(nations) {
      that.nationData = {}
      for(var i = 0; i < nations.length; i++){
        var population = nations[i].population;
        for(var j = 0; j < population.length; j++){
          if(that.nationData[population[j][0]] === undefined){
            that.nationData[population[j][0]] = []
          }
          var nation = {}
          nation["population"] = nations[i]["population"][j][1];
          nation["income"] = nations[i]["income"][j][1];
          nation["lifeExpectancy"] = nations[i]["lifeExpectancy"][j][1];
          nation["region"] = nations[i]["region"];
          nation["name"] = nations[i]["name"];

          that.nationData[population[j][0]].push(nation)
        }
      }
    });

  },
  created: function(){
  },
  methods:{
    increase: function(){
      var that = this;
      setTimeout(function(){
        that.updateGraph(1800);
        setTimeout(function(){
          that.updateGraph(1820);
        }, 1000);
      }, 1000);
      // that.updateGraph(1800);
    },
    updateGraph: function(currYear){
      var that = this;
      function x(d) { return d.income; }
      function y(d) { return d.lifeExpectancy; }
      function radius(d) { return d.population; }
      function color(d) { return d.region; }

      function order(a, b) { return radius(b) - radius(a); }
      function position(dot) {
        dot.attr("cx", function(d) { return that.xScale(x(d)); })
          .attr("cy", function(d) { return that.yScale(y(d)); })
          .attr("r", function(d) { return that.radiusScale(radius(d)); });
      }

      var svg = d3.select("svg");
      that.label.text(currYear);
      if(that.dot === undefined){
        that.dot = svg.append("g")
          .attr("class", "dots")
          .selectAll(".dot")
          .data(that.nationData[currYear])
          .enter()
          .append("circle")
          .attr("class", "dot")
          .attr("id", function(d) { 
            return (d.name)
                  .replace(/\s/g, '').replace(/\./g,'').replace(/\,/g,'')
                  .replace(/\'/g,''); 
          })
          .style("fill", function(d) { return that.colorScale(color(d)); })
          .call(position)
          .sort(order);

        that.dot.append("title").text(function(d) { return d.name; });
        that.dot.data(that.nationData[currYear]).call(position).sort(order);
        that.label.text(Math.round(currYear));
      }
      else{
        that.dot.data(that.nationData[currYear])
                .transition()
                .attr("duration", 40000)
                .attr("cx", function(d) { return that.xScale(x(d)); })
                .attr("cy", function(d) { return that.yScale(y(d)); })
                .attr("r", function(d) { return that.radiusScale(radius(d)); })
      }
    }
  },
  watch:{
  }
}
</script>

<style>
.chart {
    height: 506px;
}

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

.year.label {
    font: 500 146px "Helvetica Neue";
    fill: #ddd;
}

.year.label.active {
    fill: #aaa;
}

.overlay {
    fill: none;
    pointer-events: all;
    cursor: ew-resize;
}

.checkbox {
    position: absolute;
    dispay: inline;
    left: 1005px;
    top: 30px;
    font-family: "Helvetica Neue";
    font-size: 14px;
    color: rgb(0,128,128);
}

.explan-text {
    position: absolute;
    dispay: inline;
    left: 45px;
    top: 540px;
    width: 570px;
    font-family: "Helvetica Neue";
    font-size: "12px";
    color: black;
}
</style>