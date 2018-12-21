import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/components/index'
import HeatmapChart from '@/components/map/index'
import BubbleChart from '@/components/chart/index'
import StatisticChart from '@/components/statistic/index'
import about from '@/components/about/index'

import UsStateDemo from '@/_demo/us_state/index'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home Page',
      component: HomePage
    },
    {
      path: '/index',
      name: 'Index Page',
      component: HomePage
    },
    {
      path: '/heatmap_chart',
      name: 'Heatmap Chart Page',
      component: HeatmapChart
    },
    {
      path: '/bubble_chart',
      name: 'Bubble Chart Page',
      component: BubbleChart
    },
    {
      path: '/statistic_chart',
      name: 'Statistic Chart Page',
      component: StatisticChart
    },
    {
      path: '/about',
      name: 'About Page',
      component: about
    },
    {
      path: '/demo/us-state',
      name: 'Us Map Demo',
      component: UsStateDemo
    },
  ],
  mode: 'history'
})
