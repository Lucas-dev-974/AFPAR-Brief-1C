import request from '../../services/fetch.js'
import Chart, { TimeScale }  from 'chart.js/auto'
import PieChart from '../PieChart.vue'
import filterBar from '../filter-bar.vue'

import barChart from '../bar-chart.vue'

export default {
    components: {
        PieChart, filterBar, barChart
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
            pie_charte: null,

            showGrid: true,
            chart_title: '',

            nb_items: 10,
            years: null,

            products_for_region: []
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
                else{
                    url = '/api/regions'
                    params['regions'] = this.data_options.regions
                }
            }else if(this.on_graph == 'products'){
                this.chart_title = 'Ventes par produits'
                if(this.data_options.products.length == 0)
                    url = '/api/products/top'
                else{
                    url = '/api/products'
                    params['products'] = this.data_options.regions
                }
            }else if(this.on_graph == 'regions_products'){
                this.chart_title = 'Région'
                if(this.data_options.regions.length > 0){
                    params['regions'] = this.data_options.regions
                }

                url = '/api/regions/products'
            }
            
            
            if(this.data_options.year != null)
                params['year'] = this.data_options.year
                
            params['nb_items'] = this.nb_items
            this.getData(url, params)
        },

        getPays: async function(){
            const response    = await request.get('/api/pays')
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
            this.search()
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
            const chart = this.chart

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
                    },

                    onClick: this.clickHandler

                },
            };
        },

        clickHandler: function(evt){
            const points = this.chart.getElementsAtEventForMode(evt, 'nearest', { intersect: true }, true);

            if (points.length && this.on_graph == 'regions_products') {
                const firstPoint = points[0];
                const label = this.chart.data.labels[firstPoint.index];
                const value = this.chart.data.datasets[firstPoint.datasetIndex].data[firstPoint.index]; 

                this.pieChart(label)
            }
        },

        dataset: function(){
            let datas  = Object.values(this.response)
            let labels = Object.keys(this.response)

            if(this.on_graph == 'regions_products'){
                datas  = Object.values(this.response)
                labels = Object.keys(this.response)

                this.data_options.regions = labels
                datas = datas.map((data) =>  data['total_sold'] )
            }

            return {
                labels: Object.keys(this.response),
                datasets: [{
                    data: datas,
                    maxBarThickness: 50
                }]
            }
        },

        saveYear: function() {
            this.$refs.datepicker.activePicker  = 'YEAR'
        },


        pieChart: function(label){
            if(this.pie_charte != null) this.pie_charte.destroy()

            const canvas = document.getElementById('pie_chart')
            
            console.log(label);
            this.pie_charte = new Chart(canvas, {
                type: 'pie',
                data: this.pieChartSetup(label)
            })
        },

        pieChartSetup: function(label){
            const data = this.response[label].products

            console.log(data);
            return {
                labels: data.map(product => product.stock_code),
                datasets: [{
                  data: data.map(product => product.invoice_detail),
                  hoverOffset: 5
                }]
            };
        }
    }
}