<template>
  <div class="index">
    <h1>{{ msg }}</h1>
    </br>
    <CriminalMap/>
    </br>
    <TwitterSentiment/>
    @TODO
  </div>
</template>

<script>
const criminalMap = require('./criminal_map/index.vue').default;
const twitterSentiment = require('./twitter_sentiment/index.vue').default;

export default {
  components: {
    CriminalMap: criminalMap,
    TwitterSentiment: twitterSentiment
  },
  name: 'index-page',
  data () {
    return {
      msg: 'Index Page'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
