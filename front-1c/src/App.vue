<template>
  <v-app>
    <v-main>
      <Navbar />
      <Notif v-if="$store.state.notif.on" />
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
import Notif from './components/Notif.vue'
import Navbar from './components/navbar.vue'

export default {
  name: 'App',

  components: {
    Notif, Navbar
  },

  data: () => ({
    //
  }),
}
</script>
