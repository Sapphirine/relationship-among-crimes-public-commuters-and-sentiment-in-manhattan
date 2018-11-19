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
      currYear: 1800,
      title: "Chart Plot",
      width: 960 - margin.right,
      height: 500 - margin.top - margin.bottom,
      marginTop: margin.top,
      marginBottom: margin.bottom,
      marginLeft: margin.left,
      marginRight: margin.right,
      yearList: undefined,
    }
  },
  mounted: function(){
  },
  created: function(){
  },
  methods:{
    increase: function(){
      this.currYear += 1;
      this.updateGraph(this.currYear)
    },
    updateGraph: function(currYear) {
      var that = this;
      var margin = {top: 19.5, right: 19.5, bottom: 19.5, left: 39.5};

      var marginLeft = that.marginLeft;
      var marginRight = that.marginRight;
      var marginTop = that.marginTop;
      var marginBottom = that.marginBottom;
      var svg = d3.select(".chartHolder")
      .append("svg")
      .attr("width", that.width + marginLeft + marginRight)
      .attr("height", that.height + marginTop + marginBottom + 130);

      function x(d) { return d.income; }
      function y(d) { return d.lifeExpectancy; }
      function radius(d) { return d.population; }
      function color(d) { return d.region; }
      function key(d) { return d.name; }

      var height = that.height;
      var width = that.width;
      var margin = {top: that.marginTop,
                    right: that.marginRight,
                    bottom: that.marginBottom,
                    left: that.marginLeft
                   };

      var xScale = d3.scaleLog().domain([300, 1e5]).range([0, width]),
          yScale = d3.scaleLinear().domain([10, 85]).range([height, 0]),
          radiusScale = d3.scaleSqrt().domain([0, 5e8]).range([0, 40]),
          colorScale = d3.scaleOrdinal(d3.schemeCategory10);

      var xAxis = d3.axisBottom().scale(xScale).ticks(12, d3.format(",d"));
      var yAxis = d3.axisLeft().scale(yScale);

      var svg = d3.select("svg")
                  .append("g")
                  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

      // Add the y-axis.
      svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

      // Add an x-axis label.
      svg.append("text")
        .attr("class", "x label")
        .attr("text-anchor", "end")
        .attr("x", width)
        .attr("y", height - 6)
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
      var label = svg.append("text")
                    .attr("class", "year label")
                    .attr("text-anchor", "end")
                    .attr("y", height + 130)
                    .attr("x", width)
                    .text(currYear);

      // Load the data.
      d3.json("static/demo_data/data/nations.json").then(function(nations) {

        // A bisector since many nation's data is sparsely-defined.
        var bisect = d3.bisector(function(d) {
            return d[0];
        });

        function interpolateValues(values, year) {
          var i = bisect.left(values, year, 0, values.length - 1),
              a = values[i];
          if (i > 0) {
          var b = values[i - 1],
              t = (year - a[0]) / (b[0] - a[0]);
            return a[1] * (1 - t) + b[1] * t;
          }
          return a[1];
        }
        function interpolateData(year) {
          return nations.map(function(d) {
            return {
                name: d.name,
                region: d.region,
                income: interpolateValues(d.income, year),
                population: interpolateValues(d.population, year),
                lifeExpectancy: interpolateValues(d.lifeExpectancy, year)
            };
	        });
      	}

        function position(dot) {
            dot.attr("cx", function(d) { return xScale(x(d)); })
              .attr("cy", function(d) { return yScale(y(d)); })
              .attr("r", function(d) { return radiusScale(radius(d)); });
        }

        function order(a, b) {
            return radius(b) - radius(a);
        }

        var dot = svg.append("g")
            .attr("class", "dots")
            .selectAll(".dot")
            .data(interpolateData(currYear))
            .enter().append("circle")
            .attr("class", "dot")
            .attr("id", function(d) { return (d.name)
                    .replace(/\s/g, '').replace(/\./g,'').replace(/\,/g,'')
                    .replace(/\'/g,''); })
            .style("fill", function(d) { return colorScale(color(d)); })
            .call(position)
            .sort(order);

        var voronoi = d3.voronoi()
          .x(function(d) { return xScale(x(d)); })
          .y(function(d) { return yScale(y(d)); })
          .clipExtent([[0, 0], [width, height]]);

        var voronoiTiling =  svg.selectAll("path")
            .data(voronoi(interpolateData(currYear))) //Use voronoi() with your dataset inside
            .enter().append("path")
            .attr("d", function(d, i) {return "M" + d.join("L") + "Z"; })
            .datum(function(d, i) { return d.point; })
            .attr("id", function(d,i) { return "voronoi" + d.name.replace(/\s/g, '')
                .replace(/\./g,'')
                .replace(/\,/g,'')
                .replace(/\'/g,''); })
            .style("stroke", "rgb(0,128,128)")
            .style("visibility", d3.select("input").property("checked") ? "hidden" : "visible" )
            .style("fill", "none")
            .style("opacity", 0.5)
            .style("pointer-events", "all")
            .on("mouseover", showTooltip)
            .on("mouseout", removeTooltip);

        dot.append("title")
            .text(function(d) { return d.name; });

        var box = label.node().getBBox();

        var overlay = svg.append("rect")
          .attr("class", "overlay")
          .attr("x", box.x)
          .attr("y", box.y)
          .attr("width", box.width)
          .attr("height", box.height)
          .on("mouseover", enableInteraction);

        svg.transition()
            .duration(30000)
            .ease("linear")
            .tween("year", tweenYear)
            .each("end", enableInteraction);

        function showTooltip(d, i) {
            d3.select("#countryname").remove();
            d3.selectAll(".dot").style("opacity", 0.2);
            var circle = d3.select("#" + d.name.replace(/\s/g, '')
                .replace(/\./g,'')
                .replace(/\,/g,'')
                .replace(/\'/g,''));
            circle.style("opacity", 1);
            svg.append("text")
              .attr("id", "countryname")
              .attr("y", height - 10)
              .attr("x", 10)
              .text(d.name)
              .style("font-family", "Helvetica Neue")
              .style("font-size", 24)
              .style("fill", colorScale(color(d)));
        }
        function removeTooltip(d, i) {
            d3.selectAll(".dot").style("opacity", 1);
            d3.select("#countryname").remove();
        }
        function tweenYear() {
          return function(t) { displayYear(year(t)); };
        }
        function displayYear(year) {
          dot.data(interpolateData(year), key).call(position).sort(order);
          label.text(Math.round(year));

          //redraw voronoi
          d3.selectAll("path").remove();
          //		voronoiTiling.data(voronoi(interpolateData(year)));
          svg.selectAll("path")
            .data(voronoi(interpolateData(year))) //Use voronoi() with your dataset inside
            .enter().append("path")
            .attr("d", function(d, i) {return "M" + d.join("L") + "Z"; })
            .datum(function(d, i) { return d.point; })
              //give each cell a unique id where the unique part corresponds to the dot ids
            .attr("id", function(d,i) { return "voronoi" + d.name.replace(/\s/g, '').replace(/\./g,'').replace(/\,/g,''); })
            .style("stroke", "rgb(0,128,128)")
            .style("visibility", d3.select("input").property("checked") ? "hidden" : "visible" )
            .style("fill", "none")
            .style("opacity", 0.5)
            .style("pointer-events", "all")
            .on("mouseover", showTooltip)
            .on("mouseout", removeTooltip);
        }

        function enableInteraction() {
          var yearScale = d3.scaleLinear()
            .domain([1800, 2009])
            .range([box.x + 10, box.x + box.width - 10])
            .clamp(true);

          // Cancel the current transition, if any.
          svg.transition().duration(0);

          overlay
            .on("mouseover", mouseover)
            .on("mouseout", mouseout)
            .on("mousemove", mousemove)
            .on("touchmove", mousemove);

          function mouseover() {
            label.classed("active", true);
          }
          function mouseout() {
            label.classed("active", false);
          }
          function mousemove() {
            displayYear(yearScale.invert(d3.mouse(this)[0]));
          }
        }

      });
    }
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