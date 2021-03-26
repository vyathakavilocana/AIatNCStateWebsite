import Vue from 'vue'
import store from '@/store'
import router from '@/router'
import VueAnalytics from 'vue-analytics'
import VueRaven from 'vue-raven'
import App from '@/App.vue'
import './registerServiceWorker'
import axios from 'axios'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

Vue.config.productionTip = false

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

// Sentry for logging frontend errors
Vue.use(VueRaven, {
  dsn: process.env.VUE_APP_SENTRY_PUBLIC_DSN,
  disableReport: process.env.NODE_ENV === 'development'
})

// more info: https://github.com/MatteoGabriele/vue-analytics
Vue.use(VueAnalytics, {
  id: process.env.VUE_APP_GOOGLE_ANALYTICS,
  router
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
