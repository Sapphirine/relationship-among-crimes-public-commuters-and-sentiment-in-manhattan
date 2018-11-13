import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/components/index'

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
      path: '/demo/us-state',
      name: 'Us Map Demo',
      component: UsStateDemo
    },
  ],
  mode: 'history'
})
