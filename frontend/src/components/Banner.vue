<template>
    <div class="banner-wrapper" :class="{'start-left': start === 'left', 'start-right': start === 'right'}">
      <h1>{{ header }}</h1>
      <hr/>
      <b-container>
        <b-row style="height: 100px;">
          <b-col>
            <h6>Content 1</h6>
          </b-col>
          <b-col>
            <h6>Content 2</h6>
          </b-col>
          <b-col>
            <h6>Content 3</h6>
          </b-col>
        </b-row>
      </b-container>
      <div class="d-flex flex-row-reverse" v-if="link != null && link.text != null && link.name != null">
        <router-link :to="link.name">
          {{ link.text }}
          <b-icon-link/>
        </router-link>
      </div>
    </div>
</template>

<script>
export default {
  name: 'Banner',
  props: {
    start: { type: String, required: true },
    header: { type: String, required: true },
    link: { type: Object, required: false }
  }
}
</script>

<style scoped>
.banner-wrapper {
  background-color: white;
  padding: 0 1%;
}

.start-left {
  margin-left: 15%;
}

.start-right {
  margin-right: 15%;
}
</style>
