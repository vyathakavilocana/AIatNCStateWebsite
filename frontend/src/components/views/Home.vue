<template>
  <div class="container-fluid">
    <h1>Home</h1>
    <b-button @click="sentryTest">Test Sentry</b-button>
    <div style="height: 250px;"></div>
    <b-container fluid style="padding: 0;">
      <Banner :start="'left'" :header="'Who We Are'" :link="{name: 'announcements', text: 'See more'}"></Banner>
      <div class="banner-space"></div>
      <Banner :start="'right'" :header="'Upcoming Events'"></Banner>
      <div class="banner-space"></div>
      <Banner :start="'right'" :header="'What We Do'"></Banner>
      <div class="banner-space"></div>
      <Banner :start="'left'" :header="'Learn More'"></Banner>
      <div class="banner-space"></div>
      <Banner :start="'right'" :header="'Our Partners'"></Banner>
    </b-container>
    <div v-for="(event, i) in upcomingEvents" :key="i">
      <h1>{{ event.start.date }}</h1>
      <h1>{{ event.start.time }}</h1>
    </div>
  </div>
</template>

<script>
import Banner from '@/components/Banner'

export default {
  name: 'Home',
  components: {
    Banner
  },
  computed: {
    upcomingEvents () {
      return this.$store.state.home.upcomingEvents
    }
  },
  methods: {
    sentryTest () {
      throw new Error('Test')
    }
  },
  created () {
    this.$store.dispatch('getUpcomingEvents')
  }
}
</script>

<style scoped>
.banner-space {
  height: 100px;
}
</style>
