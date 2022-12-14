import request from '../../services/fetch.js'
import Chart, { TimeScale }  from 'chart.js/auto'
import PieChart from '../PieChart.vue'

export default {
    components: {
        PieChart
    },

    data(){
        return {
            on_graph: 'pays',
            select: {
                items: [],
                value: []
            },


            data_loaded: false,
            response: null,
            labels: null,

            data_options: {
                regions: [],
                year: null,
                products: []
            },

            chart: null,

            showGrid: true,
            chart_title: '',

            nb_items: 10,
            years: null
        }
    },

    mounted(){
        
        this.getYears()
        this.search()
        
    },

    methods: {
        search: function(){
            let url    = null
            let params = {}

            if(this.on_graph == 'pays'){
                this.getPays()
                this.chart_title = 'Ventes par régions'
                if(this.data_options.regions.length == 0){
                    url = '/api/regions/top'
                    params['regions'] = this.data_options.regions
                }
                else   {
                    url = '/api/regions'
                    params['regions'] = this.data_options.regions
                }
            }else if(this.on_graph == 'products'){
                this.chart_title = 'Ventes par produits'
                if(this.data_options.products.length == 0)
                    url = '/api/products/top'
                else   {
                    url = '/api/products'
                    params['products'] = this.data_options.regions
                }
            }else if(this.on_graph == 'regions_products'){
                this.chart_title = 'Région'
                if(this.data_options.regions.length > 0){
                    params['regions'] = tihs.data_options.regions
                }

                url = '/api/regions/products'
            }
            
            params['nb_items'] = this.nb_items
            if(this.data_options.year != null)
                params['year'] = this.data_options.year

            this.getData(url, params)
        },

        getPays: async function(){
            const response    = await request.get('/api/paès du servys')
            this.select.items = response
        },

        getYears: async function(){
            const response   = await request.get('/api/years')
            this.years = response.years
        },

        byProducts: function(){
            this.on_graph = 'products'
            this.search()
        },

        byRegions: function(){
            this.on_graph = 'pays'
            this.search()
        },

        byRegionsProducts: function(){
            this.on_graph = 'regions_products'
        },

        getData: async function(url, params){
            const response = await request.get(url, params)
            this.response  = response

            if(!this.data_loaded && response != false){
                this.buildChart()
                this.data_loaded = true
            }else{
                this.chart.destroy()
                this.buildChart()
            }
        },
        

        buildChart: function(){
            const canvas = document.getElementById('chart_container')
            this.chart   = new Chart(canvas, this.configChart())

            canvas.style.minHeight = '400px'
            canvas.style.maxWidth =  '100%'
        },

        configChart: function(){
            return {
                type: 'bar',
                data: this.dataset(),
                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    animation: false,
                    indexAxis: 'y',
                    plugins: {
                        title: {
                            display: true,
                            text: this.chart_title
                        },
                        legend: {
                            display: false,
                        },
                    },

                    scales: {
                        x: {
                            grid: {
                              display: this.showGrid
                            }
                        },
                        y: {
                            grid: {
                              display: false
                            }
                        }
                    }

                },
            };
        },

        dataset: function(){
            return {
                labels: Object.keys(this.response),
                datasets: [{
                    data: Object.values(this.response),
                    maxBarThickness: 50
                }]
            }
        },

        saveYear: function() {
            this.$refs.datepicker.activePicker  = 'YEAR'
        },

    }
}