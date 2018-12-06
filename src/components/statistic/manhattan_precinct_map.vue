<template>
  <div id="manhattan_precinct_map">
    <svg width="350" height="643.6"></svg>
  </div>
</template>

<script>
const polygonCenter = require('geojson-polygon-center')
const d3 = require('d3');
const topojson = require('topojson');

const manhattan_precinct = ["1", "5", "6", "7", "9", "10", "13", "14", "17", "18", "19", "20", "22", "23", "24", "25", "26", "28", "30", "32", "33", "34"];

// According to wiki(https://en.wikipedia.org/wiki/List_of_Manhattan_neighborhoods) and google map (search midtown manhattan)
const downtown = ["1", "5", "6", "7", "9"];
const midtown = ["10", "13", "14", "17", "18"];
const uptown = ["19", "20", "22", "24"];
const uppertown = ["23", "25", "26", "28", "30", "32", "33", "34"];
const color_arr = ["rgb(214, 39, 40)", "rgb(44, 160, 44)", "rgb(31, 119, 180)", "rgb(255, 127, 14)"];

export default {
  data: function(){
    return {
    }
  },
  mounted: function() {
    var that = this;
    var svg = d3.select("svg");
    var width = +svg.attr('width');
    var height = +svg.attr('height');
    svg.attr("width", width)
      .attr("height", height)

    const projection = d3.geoMercator()
                         .center([-73.9735, 40.78])
                         .scale(130000)
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
          .style("fill", function(d){
            let curr_precinct = d.properties.Precinct.toString();
            let color = undefined;
            if(downtown.includes(curr_precinct)){
              color = color_arr[0];
            }
            else if(midtown.includes(curr_precinct)){
              color = color_arr[1];
            }
            else if(uppertown.includes(curr_precinct)){
              color = color_arr[2];
            }
            else{
              color = color_arr[3];
            }
            return color;
          })
          .style("opacity", 0.8)
          .on('mouseover', function(d) {
            d3.select(this).transition().duration(500).style("stroke-width", 5);
          })
          .on('click', function(d) {
            d3.selectAll(".precinct").transition().duration(100).style("stroke-width", 1).style("stroke-opacity", 1).style("fill", function(d){
              let curr_precinct = d.properties.Precinct.toString();
              let color = undefined;
              if(downtown.includes(curr_precinct)){
                color = color_arr[0];
              }
              else if(midtown.includes(curr_precinct)){
                color = color_arr[1];
              }
              else if(uppertown.includes(curr_precinct)){
                color = color_arr[2];
              }
              else{
                color = color_arr[3];
              }
              return color;
            })
            d3.select(this).transition().duration(100).style("stroke-width", 10).style("stroke-opacity", .5).style("fill", "#ddd")
            that.$emit('precinctSelected', +d.properties.Precinct)
          })
          .on('mouseout', function(d) {
            d3.select(this).transition().duration(500).style("stroke-width", 1);
          });

        var count = 0;
        d3.csv("static/data/precinct_center.csv", function(data){
          if(manhattan_precinct.includes(data.precinct.toString()) == true){
            var corrd = projection([data.long, data.lat])
            svg.append('text')
              .attr("class", "noSelectableText")
              .attr("x", function(d){
                return corrd[0];
              })
              .attr("y", function(d){
                return corrd[1];
              })
              .text(data.precinct);
          }

          count++;
          if(count >= manhattan_precinct.length){
            that.$emit('mapIsReady', 'ready');
          }
        });
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
.noSelectableText {
    pointer-events: none;
}
</style>