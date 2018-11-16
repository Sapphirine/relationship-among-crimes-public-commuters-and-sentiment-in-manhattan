<template>
  <div>
    <h1>Twitter Sentiment</h1>
    <div>
      <img :src="sentimentEmoji" alt="img">
    </div>
    <div>
      <button @click="increase">Click</button>
    </div>

    <div class="sliderHolder2">
      <vue-slider 
        ref="hourSlider2"
        v-model="hourSliderValue"
        v-bind="hourSliderOption"
      >
      </vue-slider>
      <vue-slider 
        ref="monthSlider2"
        v-model="monthSliderValue"
        v-bind="monthSliderOption"
      >
      </vue-slider>
    </div>
  </div>
</template>

<script>
import vueSlider from 'vue-slider-component';
export default {
  components: {
  },
  name: 'twitter',
  data: function() {
    return {
      value: 0,
      currMonth: 1,
      currHour: 0,
      sentimentEmoji: undefined,
      sentimentEmojis: [
        "static/images/1.png",
        "static/images/2.png",
        "static/images/3.png",
        "static/images/4.png",
        "static/images/5.png",
      ],
      senmentimentData: undefined,

      hourSliderValue: undefined,
      monthSliderValue: undefined,

      monthSliderOption:{
        width: 'auto',
        tooltip: "always",
        disable: false,
        piecewise: true,
        piecewiseLabel: true,
        startAnimation: true,
        data:[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
      },
      hourSliderOption:{
        width: 'auto',
        tooltip: "always",
        disable: false,
        piecewise: true,
        piecewiseLabel: true,
        startAnimation: true,
        data:[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
      }
    }
  },

  watch: {
    hourSliderValue: {
      handler: function(){
        console.log("hour sliderValue change")
        var that = this;
        that.currHour = that.hourSliderValue;
        this.updateSentiment();
      }
    },
    monthSliderValue: {
      handler: function(){
        console.log("hour sliderValue change")
        var that = this;
        that.currMonth = that.monthSliderValue;
        this.updateSentiment();
      }
    },
    immediate: true,
  },
  created: function(){
    var that = this;

    that.senmentimentData = {};

    fakeData = {
      1:{
        0:{"Sentiment": -1.0  },
        1:{"Sentiment": -0.9  },
        2:{"Sentiment": -0.8  },
        3:{"Sentiment": -0.7  },
        4:{"Sentiment": -0.6  },
        5:{"Sentiment": -0.55 },
        6:{"Sentiment": -0.54 },
        7:{"Sentiment": -0.53 },
        8:{"Sentiment": -0.52 },
        9:{"Sentiment": -0.51 },
        10:{"Sentiment": -0.5 },
        11:{"Sentiment": -0.49},
        12:{"Sentiment": -0.48},
        13:{"Sentiment": -0.4 },
        14:{"Sentiment": -0.3 },
        15:{"Sentiment": -0.2 },
        16:{"Sentiment": -0.1 },
        17:{"Sentiment": -0.05},
        18:{"Sentiment": 0.01 },
        19:{"Sentiment": 0.0  },
        20:{"Sentiment": 0.05 },
        21:{"Sentiment": 0.1  },
        22:{"Sentiment": 0.2  },
        23:{"Sentiment": 0.3  }
      },
      2:{
        0:{"Sentiment": 0.35 },
        1:{"Sentiment": 0.4  },
        2:{"Sentiment": 0.45 },
        3:{"Sentiment": 0.46 },
        4:{"Sentiment": 0.47 },
        5:{"Sentiment": 0.48 },
        6:{"Sentiment": 0.49 },
        7:{"Sentiment": 0.50 },
        8:{"Sentiment": 0.51 },
        9:{"Sentiment": 0.52 },
        10:{"Sentiment": 0.53},
        11:{"Sentiment": 0.6 },
        12:{"Sentiment": 0.7 },
        13:{"Sentiment": 0.8 },
        14:{"Sentiment": 0.9 },
        15:{"Sentiment": 0.91},
        16:{"Sentiment": 0.92},
        17:{"Sentiment": 0.93},
        18:{"Sentiment": 0.94},
        19:{"Sentiment": 0.95},
        20:{"Sentiment": 0.97},
        21:{"Sentiment": 0.98},
        22:{"Sentiment": 0.99},
        23:{"Sentiment": 1.0 }
      },
    };

    // d3.csv("static/data/sentiment.csv", function(data){
    // });
    that.senmentimentData = fakeData;
    
  },
  mounted: function(){
    this.sentimentEmoji = this.sentimentEmojis[2];
    this.$refs.hourSlider2.setIndex(12);
    this.$refs.monthSlider2.setIndex(1);
  },
  methods:{
    increase:function(){
      this.value ++;
      this.sentimentEmoji = this.sentimentEmojis[this.value%5]
    },
    updateSentiment: function(){
      var sentimentValue =  this.sentimentEmojis[this.senmentimentData[this.currMonth][this.currHour]["Sentiment"]]

      if(sentimentValue >= -1.0 && Sentiment < -0.75){
        this.sentimentEmoji = this.sentimentEmojis[4];
      }
      else if(sentimentValue >= -0.75 && sentimentValue < -0.25){
        this.sentimentEmoji = this.sentimentEmojis[3];
      }
      else if(sentimentValue >= -0.25 && sentimentValue < 0.25){
        this.sentimentEmoji = this.sentimentEmojis[2];
      }
      else if(sentimentValue >= 0.25 && sentimentValue < 0.75){
        this.sentimentEmoji = this.sentimentEmojis[1];
      }
      else if(sentimentValue >= 0.75 && sentimentValue < 1.0){
        this.sentimentEmoji = this.sentimentEmojis[0];
      }
    },
  }
}
</script>

<style>
img{
  width: 500px;
  height: 500px;
}
</style>