<template>
  <div id="manhattan_map">
    <div class="row">
      <div id="map_criminal_col" class="cliente">
        <svg id="map_svg_criminal" width="500" height="600"></svg>
      </div>
      <div class="ml-3 mr-3">
      </div>
      <div id="map_traffic_col" class="cliente">
        <svg id="map_svg_traffic" width="500" height="600"></svg>
      </div>
    </div>
  </div>
</template>

<script>
const polygonCenter = require('geojson-polygon-center')
const d3 = require('d3');
const topojson = require('topojson');

export default {
  mounted: function() {
    var that = this;
    var svg_criminal = d3.select("#map_svg_criminal");
    var svg_traffic = d3.select("#map_svg_traffic");
    var width = +svg_criminal.attr('width');
    var height = +svg_criminal.attr('height');

    const projection = d3.geoMercator()
                         .center([-73.94, 40.78])
                         .scale(130000)
                         .translate([width/2, height/2]);
    var path = d3.geoPath().projection(projection);

    d3.json("static/data/police_precincts.geojson")
      .then(function(geoJson) {
        svg_criminal.append('g')
          .selectAll('.precinct_criminal')
          .data(geoJson.features)
          .enter()
          .append("path")
          .attr("class", "precinct_criminal")
          .attr("class", function(d){
            return "nb" + d.properties.Precinct;
          })
          .attr("d", path)
          .classed("precinct_criminal", true)
          .on('mouseover', function(d) {
            d3.select(this).transition().duration(500).style("stroke-width", 3).style("stroke-opacity", .5);
            that.$emit('precinctSelected', +d.properties.Precinct)
          })
          .on('mouseout', function(d) {
            d3.select(this).transition().duration(500).style("stroke-width", 1).style("stroke-opacity", 1);
            that.$emit('precinctDeselected', +d.properties.Precinct)
          });

        svg_traffic.append('g')
          .selectAll('.precinct_traffic')
          .data(geoJson.features)
          .enter()
          .append("path")
          .attr("class", "precinct_traffic")
          .attr("class", function(d){
            return "nb" + d.properties.Precinct;
          })
          .attr("d", path)
          .classed("precinct_traffic", true)
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
            var bars = svg_criminal
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
          })
        that.$emit('mapIsReady', 'ready');
    });
  }
}

</script>

<style>
.precinct_criminal, .precinct_traffic{ 
  stroke: grey;
  stroke-width: 1px;
  fill: white;
}

.cliente {
  border: #cdcdcd medium solid;
  border-radius: 10px;
  -moz-border-radius: 10px;
  -webkit-border-radius: 10px;
}
</style>