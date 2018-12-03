<template>
  <div id="newyork_map">
    <h2>New York Map</h2>
    <svg width="800" height="800"></svg>
  </div>
</template>

<script>
const polygonCenter = require('geojson-polygon-center')
const d3 = require('d3');
const topojson = require('topojson');

const manhattan_precinct = ["1", "5", "6", "7", "9", "10", "13", "14", "17", "18", "19", "20", "22", "23", "24", "25", "26", "28", "30", "32", "33", "34"];

export default {
  mounted: function() {
    var that = this;
    var svg = d3.select("svg");
    var width = +svg.attr('width');
    var height = +svg.attr('height');

    const projection = d3.geoMercator()
                         .center([-73.94, 40.78])
                         .scale(170000)
                         .translate([width/2, height/2]);
    var path = d3.geoPath().projection(projection);

    d3.json("static/data/police_precincts.geojson")
      .then(function(geoJson) {
        svg.append('g')
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
          .on('mouseover', function(d) {
            d3.select(this).transition().duration(500).style("stroke-width", 8).style("stroke-opacity", .5)
            that.$emit('precinctSelected', +d.properties.Precinct)
          })
          .on('mouseout', function(d) {
            d3.select(this).transition().duration(500).style("stroke-width", 1).style("stroke-opacity", 1);
            that.$emit('precinctDeselected', +d.properties.Precinct)
          });

        that.$emit('mapIsReady', 'ready');
      }
    );
  }
}

</script>

<style>
.precinct{ 
  stroke: grey;
  stroke-width: 1px;
  fill: #ddd;
}
</style>