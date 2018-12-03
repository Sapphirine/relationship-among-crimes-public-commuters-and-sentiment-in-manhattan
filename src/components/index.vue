<template>
  <div class="Index">
    <div class="container">
      <div class="row">
        <h1>{{title}}</h1>
      </div>
      <div class="row my-4">
        <div class="col-md-4">
          <div class="card mx-auto">
            <img class="card-img-top" src="https://via.placeholder.com/150" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">Map Plot</h5>
              <p class="card-text">This visualization is heapmaps of dynamic # of crimes and # of commuters of Manhattan, aggregated by precinct. Twitter is used to analyse the sentiment of manhattan people hour-by-hour in an average week.</p>
              <a href="/map_plot" class="btn btn-primary">Go Map Plot</a>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card mx-auto">
            <img class="card-img-top" src="https://via.placeholder.com/150" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">Chart Plot</h5>
              <p class="card-text">This visualizationis the bubble plot of # of crimes and # commuters, the size of bubble denotes the # of residents, and color of bubbles represents the area. We measure the correlation using pearson algorithm.</p>
              <a href="/chart_plot" class="btn btn-primary">Go Chart Plot</a>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card mx-auto" >
            <img class="card-img-top" src="https://via.placeholder.com/150" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">Statistic Plot</h5>
              <p class="card-text">This visualizationis the bubble plot of # of crimes and # commuters, the size of bubble denotes the # of residents, and color of bubbles represents the area. We measure the correlation using pearson algorithm.</p>
              <a href="/statistic_plot" class="btn btn-primary">Go Statistic Plot</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Index Page',
  data: function() {
    return {
      title: "Relationship between the number of crimes and the number of commuters in Manhattan"
    }
  }
}
</script>

<style>
</style>