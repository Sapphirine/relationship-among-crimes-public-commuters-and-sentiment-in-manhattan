import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/components/index'
import MapPlot from '@/components/map/index'
import ChartPlot from '@/components/chart/index'
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
      path: '/map_plot',
      name: 'Map Plot Page',
      component: MapPlot
    },
    {
      path: '/chart_plot',
      name: 'Chart Plot Page',
      component: ChartPlot
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
