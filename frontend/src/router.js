import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/components/views/Home'
import About from '@/components/views/About'
import Events from '@/components/views/Events'
import Contact from '@/components/views/Contact'
import EventsHome from '@/components/event/EventsHome'
import EventsArchive from '@/components/event/EventsArchive'

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/about',
    component: About
  },
  {
    path: '/events',
    component: Events,
    children: [
      {
        path: '',
        component: EventsHome
      },
      {
        path: 'archive',
        component: EventsArchive
      }
    ]
  },
  {
    path: '/contact',
    component: Contact
  }
]

Vue.use(VueRouter)
const router = new VueRouter({
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 }
  },
  mode: 'history',
  base: '/',
  routes
})

export default router
