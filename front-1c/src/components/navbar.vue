<template>
    <nav class="w-100 d-flex justify-center align-center" id="navbar">
        <p>Analysis Features Preprocessing And Research</p>
    </nav>
</template>

<script>
 import request from '../plugins/fetch.js'
export default{

    data(){
        return{

        }
    },

    mounted(){
        this.checkConnexion()
    },

    methods: {
        checkConnexion: async function(){
            const response = await request.get('/api/auth/check')
            if(!window.location.href.includes('login'))
                if(!response) window.location.href = '/login'
        }
    }
}
</script>