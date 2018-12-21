<template>
  <div class="chart_plot">
    <div class="container">
      <h1 class="my-4">About Us</h1>
      <div class="row">
        <div class="col-lg-12">
          <h2 class="my-6">Team</h2>
        </div>
      </div>
      <div class="row">
        <div class="col-lg-4 col-sm-6 text-center mb-4">
          <img class="rounded-circle d-block mx-auto" width=150 height=200 src="static/images/yl.png" alt="">
          <h3 class="my-4">Yunan Lu</h3>
          <p>UNI: yl4021</p>
          <p>Electrical Engineering</p>
          <button class="btn btn-primary" v-on:click="directToLinkedin('https://www.linkedin.com/in/luyunan/')">linkedin</button>
        </div>
        <div class="col-lg-4 col-sm-6 text-center mb-4">
          <img class="rounded-circle d-block mx-auto" width=150 height=200 src="static/images/zd.png" alt="">
          <h3 class="my-4">Zhicheng Ding</h3>
          <p>UNI: zd2212</p>
          <p>Computer Science</p>
          <button class="btn btn-primary" v-on:click="directToLinkedin('https://www.linkedin.com/in/zhicheng-ding/')">linkedin</button>
        </div>
        <div class="col-lg-4 col-sm-6 text-center mb-4">
          <img class="rounded-circle d-block mx-auto" width=150 height=200 src="static/images/lb.png" alt="">
          <h3 class="my-4">Lin Bai</h3>
          <p>UNI: lb3161</p>
          <p>Electrical Engineering</p>
          <button class="btn btn-primary" v-on:click="directToLinkedin('https://www.linkedin.com/in/linbai023/')">linkedin</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'about',
  data: function() {
    return {
    }
  },
  methods:{
    directToLinkedin: function(link){
      window.location = link;
    }
  },
}
</script>

<style>
</style>