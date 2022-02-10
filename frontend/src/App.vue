<template lang="html">
  <div id="root" style="height: 3000px;">
    <Navbar id="navbar"></Navbar>
    <router-view id="viewport"/>
    <BackgroundCanvas></BackgroundCanvas>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar'
import BackgroundCanvas from '@/components/BackgroundCanvas'

export default {
  name: 'App',
  components: {
    Navbar,
    BackgroundCanvas
  }
}
</script>

<style lang="scss">
  // Import custom theme
  @import 'assets/theme.scss';

  // Set transparent background for main viewport
  #viewport {
    background-color: transparent;
    padding: 0;
  }

  // Import Bootstrap and BootstrapVue source SCSS files
  @import '~bootstrap/scss/bootstrap.scss';
  @import '~bootstrap-vue/src/index.scss';

  // Ensure document body isn't cropped
  body {
    overflow: auto;
  }
</style>
