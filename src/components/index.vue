<template>
  <div class="Index">
    <div class="container">
      <div class="row">
        <h1>{{title}}</h1>
      </div>
      <div class="row my-4">
        <div class="col-md-4">
          <div class="card mx-auto">
            <img class="card-img-top" src="/static/images/map_plot.png" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">Map Plot (Step 1)</h5>
              <hr>
              <p class="card-text">This visualization is heapmaps of dynamic # of crimes and # of commuters of Manhattan, aggregated by precinct. Twitter is used to analyse the sentiment of manhattan people hour-by-hour in an average week.</p>
              <a href="/map_plot" class="btn btn-primary">Go to Map Plot</a>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card mx-auto">
            <img class="card-img-top" src="/static/images/chart_plot.png" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">Chart Plot (Step 2)</h5>
              <hr>
              <p class="card-text">This visualizationis the bubble plot of # of crimes and # commuters, the size of bubble denotes the # of residents, and color of bubbles represents the area. We measure the correlation using pearson algorithm.</p>
              <a href="/chart_plot" class="btn btn-primary">Go to Chart Plot</a>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card mx-auto" >
            <img class="card-img-top" src="/static/images/statistic_plot.png" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">Statistic Plot (Step 3)</h5>
              <hr>
              <p class="card-text">This visualizationis summerize the overall statistic data. We show the daily trend of crime and commuters of different precinct. Also we explore the trend of sentiment and correlation between # of crime and # of commuters.</p>
              <a href="/statistic_plot" class="btn btn-primary">Go to Statistic Plot</a>
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
      title: "Relationship among Crimes, Commuters, and Sentiment in Manhattan"
    }
  }
}
</script>

<style>
</style>