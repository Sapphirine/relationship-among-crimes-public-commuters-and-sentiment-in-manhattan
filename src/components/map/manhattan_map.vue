<template>
  <div id="manhattan_map">
    <svg id="map_svg" width="800" height="600"></svg>
  </div>
</template>

<script>
const polygonCenter = require('geojson-polygon-center')
const d3 = require('d3');
const topojson = require('topojson');

export default {
  mounted: function() {
    var that = this;
    var svg = d3.select("svg");
    var width = +svg.attr('width');
    var height = +svg.attr('height');

    const projection = d3.geoMercator()
                         .center([-73.94, 40.78])
                         .scale(130000)
                         .translate([width/2, height/2]);
    var path = d3.geoPath().projection(projection);

    d3.json("static/data/police_precincts.geojson")
      .then(function(geoJson) {
        svg.append('g')
          .selectAll('.precinct')
          .data(geoJson.features)
          .enter()
          .append("path")
          .attr("class", "precinct")
          .attr("class", function(d){
            return "nb" + d.properties.Precinct;
          })
          .attr("d", path)
          .classed("precinct", true)
          .on('mouseover', function(d) {
            d3.select(this).transition().duration(500).style("stroke-width", 3).style("stroke-opacity", .5);
            that.$emit('precinctSelected', +d.properties.Precinct)
          })
          .on('mouseout', function(d) {
            d3.select(this).transition().duration(500).style("stroke-width", 1).style("stroke-opacity", 1);
            that.$emit('precinctDeselected', +d.properties.Precinct)
          });

        d3.csv("static/data/precinct_center.csv")
          .then(function(geoCenter) {

            var bars = svg.selectAll(".precinctCenter")
              .data(geoCenter)
              .enter()
              .append("g")
              .attr("class", function(d){
                return "bars " + d.precinct;
              })
              .attr("transform", function(d) {
                return "translate(" + projection([d.long, d.lat]) + ")";
              })
              .append("rect");

          that.$emit('mapIsReady', 'ready');
        })
      }
    );
  }
}

</script>

<style>
.precinct{ 
  stroke: grey;
  stroke-width: 1px;
}
</style>