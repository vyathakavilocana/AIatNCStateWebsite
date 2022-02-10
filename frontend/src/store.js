import Vue from 'vue'
import Vuex from 'vuex'

import { getAPI } from '@/main'

Vue.use(Vuex)

const store = new Vuex.Store({
  strict: true,
  state: {
    home: {
      recentAnnouncements: [],
      upcomingEvents: [],
      recentProjects: [],
      affiliates: []
    }
  },
  mutations: {
    setRecentAnnouncements (state, { announcements }) {
      state.home.recentAnnouncements = announcements
    },
    setUpcomingEvents (state, { events }) {
      state.home.upcomingEvents = events
    },
    setRecentProjects (state, { projects }) {
      state.home.recentProjects = projects
    },
    setAffiliates (state, { affiliates }) {
      state.home.affiliates = affiliates
    }
  },
  actions: {
    getRecentAnnouncements (context) {
      return new Promise((resolve, reject) => {
        getAPI.get('/events/announcements/?count=3')
          .then(response => {
            context.commit('setRecentAnnouncements', {
              announcements: response.data
            })
            resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    getUpcomingEvents (context) {
      return new Promise((resolve, reject) => {
        getAPI.get('/events/upcoming/?count=3')
          .then(response => {
            context.commit('setUpcomingEvents', {
              events: response.data
            })
            resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    getRecentProjects (context) {
      return new Promise((resolve, reject) => {
        // TODO: API endpoint/query parameters not yet implemented
        getAPI.get('/projects/?count=2&sort=updated')
          .then(response => {
            context.commit('setRecentProjects', {
              projects: response.data
            })
            resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    getAffiliates (context) {
      return new Promise((resolve, reject) => {
        getAPI.get('/affiliates/')
          .then(response => {
            context.commit('setAffiliates', {
              affiliates: response.data
            })
            resolve()
          })
          .catch(err => {
            reject(err)
          })
      })
    }
  }
})

export default store
