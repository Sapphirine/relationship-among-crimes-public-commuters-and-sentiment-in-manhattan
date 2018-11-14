<template>
  <div id="newyork_map">
    <h2>New York Map</h2>
    <svg width="800" height="800"></svg>
  </div>
</template>

<script>
const polygonCenter = require('geojson-polygon-center')
// var gju = require('geojson-utils');
const d3 = require('d3');
const topojson = require('topojson');

export default {
  mounted: function() {
    var that = this;
    var svg = d3.select("svg");
    var width = +svg.attr('width');
    var height = +svg.attr('height');

    const projection = d3.geoMercator()
                         .center([-73.94, 40.70])
                         .scale(50000)
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

        var bars = svg.selectAll(".precinctCenter")
            .data(function(){
               var geoCenter = [];
               for(var i = 0; i < geoJson.features.length; i++) {
                 var dic = {}
                 dic["precinct"] = geoJson.features[i].properties.Precinct;
                 dic["center"] = (polygonCenter(geoJson.features[i]));
                 geoCenter.push(dic);
               }
               geoCenter[0]["center"]["coordinates"][0] = -74.006973
               geoCenter[0]["center"]["coordinates"][1] = 40.720382

              geoCenter[74]["center"]["coordinates"][0] = -74.106616
              geoCenter[74]["center"]["coordinates"][1] = 40.588817

               40.720382
               console.log(geoCenter)
               return geoCenter;
            })
            .enter()
            .append("g")
            .attr("class", "bars")
            .attr("transform", function(d) {
              return "translate(" + projection(d.center.coordinates) + ")";
             });
        console.log(bars)
        bars.append("rect")
            .attr('height',  function(d) {return 50})
            .attr('width', 5)
            .attr('y', function(d) {return -(50)})
            .attr("class", "bars")
            .style("fill", "blue")
            .style("stroke", "white")
            .style("stroke-width", 1)
            .style("opacity", 0.7)
            ;

        that.$emit('mapIsReady', 'ready');
      }
    );
  }
  // TODO: fire events
}
</script>

<style>
.precinct{ 
  stroke: grey;
  stroke-width: 1px;
}
</style>