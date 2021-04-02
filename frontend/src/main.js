import Vue from 'vue'
import * as Sentry from '@sentry/vue'
import { Integrations } from '@sentry/tracing'
import store from '@/store'
import router from '@/router'
import VueAnalytics from 'vue-analytics'
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
Sentry.init({
  Vue: Vue,
  dsn: process.env.VUE_APP_SENTRY_PUBLIC_DSN,
  integrations: [new Integrations.BrowserTracing()],

  // Set tracesSampleRate to 1.0 to capture 100% of transactions for performance monitoring.
  // We recommend adjusting this value in production
  tracesSampleRate: 1.0,
  tracingOptions: {
    trackComponents: true
  },
  debug: Boolean(process.env.VUE_APP_SENTRY_DEBUG)
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
