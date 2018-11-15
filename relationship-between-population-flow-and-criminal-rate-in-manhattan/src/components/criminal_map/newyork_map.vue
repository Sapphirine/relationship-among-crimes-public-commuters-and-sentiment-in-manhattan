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

            // Hardcore some geoCenter using the coordinate from Google Map since the polygenCenter need that polygen connected (if precinct with island, it fails to compute the result). 
            geoCenter[0]["center"]["coordinates"][0] = -74.006973
            geoCenter[0]["center"]["coordinates"][1] = 40.720382

            geoCenter[8]["center"]["coordinates"][0] = -73.970820
            geoCenter[8]["center"]["coordinates"][1] = 40.756937

            geoCenter[15]["center"]["coordinates"][0] = -73.941132
            geoCenter[15]["center"]["coordinates"][1] = 40.801098

            geoCenter[22]["center"]["coordinates"][0] = -73.925368
            geoCenter[22]["center"]["coordinates"][1] = 40.810569

            geoCenter[23]["center"]["coordinates"][0] = -73.895629
            geoCenter[23]["center"]["coordinates"][1] = 40.816424

            geoCenter[27]["center"]["coordinates"][0] = -73.827296
            geoCenter[27]["center"]["coordinates"][1] = 40.83107

            geoCenter[29]["center"]["coordinates"][0] = -73.847437
            geoCenter[29]["center"]["coordinates"][1] = 40.887754

            geoCenter[30]["center"]["coordinates"][0] = -73.900396
            geoCenter[30]["center"]["coordinates"][1] = 40.844155

            geoCenter[33]["center"]["coordinates"][0] = -73.879678
            geoCenter[33]["center"]["coordinates"][1] = 40.869286

            geoCenter[37]["center"]["coordinates"][0] = -73.941588
            geoCenter[37]["center"]["coordinates"][1] = 40.628193

            geoCenter[41]["center"]["coordinates"][0] = -73.905097
            geoCenter[41]["center"]["coordinates"][1] = 40.64882

            geoCenter[46]["center"]["coordinates"][0] = -73.881488
            geoCenter[46]["center"]["coordinates"][1] = 40.671378

            geoCenter[51]["center"]["coordinates"][0] = -73.924286
            geoCenter[51]["center"]["coordinates"][1] = 40.689894

            geoCenter[54]["center"]["coordinates"][0] = -73.960528
            geoCenter[54]["center"]["coordinates"][1] = 40.690305

            geoCenter[57]["center"]["coordinates"][0] = -73.816488
            geoCenter[57]["center"]["coordinates"][1] = 40.586525

            geoCenter[63]["center"]["coordinates"][0] = -73.839768
            geoCenter[63]["center"]["coordinates"][1] = 40.682496

            geoCenter[70]["center"]["coordinates"][0] = -73.775763
            geoCenter[70]["center"]["coordinates"][1] = 40.679988

            geoCenter[71]["center"]["coordinates"][0] = -73.915272
            geoCenter[71]["center"]["coordinates"][1] = 40.769531

            geoCenter[73]["center"]["coordinates"][0] = -74.077465
            geoCenter[73]["center"]["coordinates"][1] = 40.644822

            geoCenter[74]["center"]["coordinates"][0] = -74.106616
            geoCenter[74]["center"]["coordinates"][1] = 40.588817

            return geoCenter;
          })
          .enter()
          .append("g")
          .attr("class", function(d){
            return "bars " + d.precinct;
          })
          .attr("transform", function(d) {
            return "translate(" + projection(d.center.coordinates) + ")";
          })
          .append("rect");

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