import request from '../../plugins/fetch.js'

export default{
    data(){
        return {
            username: '',
            password: ''
        }
    },

    mounted(){

    },

    methods: {
        login: async function(){
            const response = await request.post('/api/auth/login', { username: this.username, password: this.password })

            if(!response) return false

            this.$store.commit('updateToken', response.token)
            this.$store.commit('setUser', response.user)

            window.location.href = '/'
        }
    }
}