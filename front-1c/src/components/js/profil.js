export default{
    methods: {
        logout: function(){
            this.$store.commit('updateToken', null)
            window.location.href = '/login'
        }
    }
}