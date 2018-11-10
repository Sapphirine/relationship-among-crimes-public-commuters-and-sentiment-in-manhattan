import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import CriminalMap from '@/components/CriminalMap'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/criminalmap',
      name: 'CriminalMap',
      component: CriminalMap
    },
  ]
})
