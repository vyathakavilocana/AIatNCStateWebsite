<template>
  <b-navbar v-once toggleable="lg" type="dark" variant="primary" class="mb-1">
    <b-navbar-brand :to="{ name: 'home' }" class="pb-2">
      <b-img src="img/logo/logo.png" height="50px"/>
      AI at NC State
    </b-navbar-brand>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-item :to="{ name: 'home' }">Home</b-nav-item>
        <b-nav-item :to="{ name: 'announcements' }">Announcements</b-nav-item>
        <b-nav-item-dropdown text="Events" right>
          <b-dropdown-item :to="{ name: 'eventsHome' }">Schedule</b-dropdown-item>
          <b-dropdown-item :to="{ name: 'eventsArchive' }">Archive</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item :to="{ name: 'projects' }">Projects</b-nav-item>
        <b-nav-item :to="{ name: 'contact' }">Contact</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: 'Navbar'
}
</script>

<style scoped>
a {
  color: var(--secondary);
  text-decoration-color: var(--light);
}
</style>
