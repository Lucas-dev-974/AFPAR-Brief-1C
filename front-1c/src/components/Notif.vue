<template>
    <div style="width: fit-content; position:absolute; right: 10px; top: 80px" >
        <v-alert v-model="alert" :color="color" closable @click='close'>
            <div class="d-flex justify-space-between">
                <div class="bg-dark">{{message}}</div>
            </div>
        </v-alert>
    </div>	
</template>
    
<script>
export default{
    data(){
        return{
            message: this.$store.state.notif.message,
            alert:   this.$store.state.notif.on,
            color:   this.$store.state.notif.color
        }
    },


    methods: {
        close(){
            this.$store.commit('Notif', { alert: false })
        }
    }
}
</script>