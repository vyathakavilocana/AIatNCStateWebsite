<template lang="html">
  <div>
    <Navbar></Navbar>
    <router-view id="viewport"/>
    <div id="gradient"></div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar'

export default {
  name: 'App',
  components: {
    Navbar
  }
}
</script>

<style lang="scss">
  // Import custom theme
  @import 'assets/theme.scss';

  // Set transparent background for main viewport
  #viewport {
    background-color: transparent;
  }

  // Custom gradient background
  #gradient {
    z-index: -1;
    background-image: linear-gradient(30deg, $purple1, $purple2, $green4, $green3, $blue3, $blue1);
    height: 3000px;
    width: 100%;
    position: absolute;
    top: 0;
  }

  // Import Bootstrap and BootstrapVue source SCSS files
  @import '~bootstrap/scss/bootstrap.scss';
  @import '~bootstrap-vue/src/index.scss';
</style>
