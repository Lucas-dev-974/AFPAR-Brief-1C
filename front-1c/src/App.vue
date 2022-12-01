<template>
  <v-app>
    <v-main>
      <Notif v-if="$store.state.notif.on" />
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
import Notif from './components/Notif.vue'

export default {
  name: 'App',

  components: {
    Notif
  },

  data: () => ({
    //
  }),
}
</script>
