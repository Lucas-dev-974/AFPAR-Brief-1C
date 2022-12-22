import request from '../../services/fetch.js'

export default {
    data(){
        return {
            nb_items:   this.$store.state.nb_items,
            year_model: this.$store.state.year_select.model,
            on_graph:   this.$store.state.on_graph,
            pays:       this.$store.state.pays_select.model
        }
    },

    watch: {
        year_model: function(new_, old){ this.$store.commit('yearUpdateModel', new_) },
        nb_items:   function(new_, old){ this.$store.commit('nbItemUpdate',    new_) },
        pays:       function(new_, old){ this.$store.commit('paysUpdateModel', new_) },

        on_graph:   function(new_, old){ this.$store.commit('updateGraph', new_ ) }
    },  

    mounted(){
        this.$store.dispatch('getYears')
        this.$store.dispatch('getPays')

        this.search()
    },

    methods: {
        search: function(){
            let url    = null
            let params = {}

            // If search is on pays
            if(this.on_graph == 'pays'){
                // this.chart_title = 'Ventes par régions'
                if(this.pays.length == 0) url = '/api/regions/top'
                else{
                    url = '/api/regions'
                    params['regions'] = this.pays
                }


            }else if(this.on_graph == 'products'){
                // this.chart_title = 'Ventes par produits'
                if(this.data_options.products.length == 0) url = '/api/products/top'

                else{
                    url = '/api/products'
                    params['products'] = this.data_options.regions
                }

            }else if(this.on_graph == 'regions_products'){
                // this.chart_title = 'Région'
                if(this.pays.length > 0)
                    params['regions'] = this.pays
                

                url = '/api/regions/products'
            }
            
            
            params['year']     = this.year_model
            params['nb_items'] = this.nb_items
            
            this.getData(url, params)
        },

        getData: async function(url, params){
            const response = await request.get(url, params)
            console.log(response); 
        },

        byProducts: function(){
            this.on_graph = 'products'
            // this.search()
        },

        byRegions: function(){
            this.on_graph = 'pays'
            // this.search()
        },

        byRegionsProducts: function(){
            this.on_graph = 'regions_products'
            // this.search()
        },




    },
}