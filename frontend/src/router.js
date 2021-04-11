import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/components/views/Home'
import Announcements from '@/components/views/Announcements'
import Events from '@/components/views/Events'
import EventsHome from '@/components/event/EventsHome'
import EventsArchive from '@/components/event/EventsArchive'
import Projects from '@/components/views/Projects'
import Contact from '@/components/views/Contact'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/announcements',
    name: 'announcements',
    component: Announcements
  },
  {
    path: '/events',
    component: Events,
    children: [
      {
        path: '',
        name: 'eventsHome',
        component: EventsHome
      },
      {
        path: 'archive',
        name: 'eventsArchive',
        component: EventsArchive
      }
    ]
  },
  {
    path: '/projects',
    name: 'projects',
    component: Projects
  },
  {
    path: '/contact',
    name: 'contact',
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
