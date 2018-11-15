<template>
  <div>
    <h1>Twitter Sentiment</h1>
    Current Value  {{value}}
    <div>
      <img :src="img" alt="img">
    </div>
    <div>
      <button @click="increase">Click</button>
    </div>
  </div>
</template>

<script>
export default {
  components: {
  },
  name: 'twitter',
  data: function() {
    return {
      value: 0,
      img: undefined,
      imgs: [
        "static/images/1.png",
        "static/images/2.png",
        "static/images/3.png",
        "static/images/4.png",
      ],
    }
  },
  methods:{
    increase:function(){
      this.value ++;
      this.img = this.imgs[this.value%4]
    }
  }
}
</script>

<style>
    
</style>