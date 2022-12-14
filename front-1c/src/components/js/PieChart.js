export default {
    data(){
        return {

        }
    },

    mounted(){
        try{
            this.pieChart()
        }catch(error){
            
        }
    },  

    methods: {
        pieChart: function(){
            const canvas = document.getElementById('regions_products')
            console.log(canvas);
        }
    }
}