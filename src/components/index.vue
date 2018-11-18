<template>
  <div class="Index">
    <div class="container">
      <div class="row">
        <h1>{{title}}</h1>
      </div>
      <div class="row my-4">
        <div class="col">
          <div class="card mx-auto" style="width: 25rem;">
            <img class="card-img-top" src="https://via.placeholder.com/150" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">Map Plot</h5>
              <p class="card-text">@TODO</p>
              <a href="/map_plot" class="btn btn-primary">Go Map Plot</a>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card mx-auto" style="width: 25rem;">
            <img class="card-img-top" src="https://via.placeholder.com/150" alt="Card image cap">
            <div class="card-body">
              <h5 class="card-title">Chart Plot</h5>
              <p class="card-text">@TODO</p>
              <a href="/chart_plot" class="btn btn-primary">Go Chart Plot</a>
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
      title: "Relationship between population and criminal rate in manhattan"
    }
  }
}
</script>

<style>
</style>