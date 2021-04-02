<template>
  <div class="container">
    <h1>Home</h1>
    <b-button @click="sentryTest">Test Sentry</b-button>
  </div>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    sentryTest () {
      throw new Error('Test')
    }
  }
}
</script>

<style scoped>

</style>
