import { createStore } from 'vuex'
import VuexPersist from 'vuex-persist'
import chartStore from './chart-store.js'
import filterStore from './filtering.js'

const VuexLocalStorage = new VuexPersist({
  key:     'vuex',
  storage: window.localStorage
})

export default createStore({
  plugins: [ VuexLocalStorage.plugin ],

  state: {
    backend_host: 'http://127.0.0.1:8000',

    notif: {
      on: false,
      color: '',
      message: ''
    },

    token: null,
    user:  null,

    ...chartStore.state,
    ...filterStore.state
  },

  mutations: {
    Notif(state, notifData){
      if(notifData.on){
          state.notif.on      = true
          state.notif.message = notifData.message
          state.notif.color   = notifData.color
      }else{
          state.notif.on = false
      }
    }, 

    updateToken: function(state, token){
      state.token = token
    },

    setUser: function(state, user){
      state.user = user
    },

    ...chartStore.mutations,
    ...filterStore.mutations
  },

  actions: {
    ...filterStore.actions
  }
})
