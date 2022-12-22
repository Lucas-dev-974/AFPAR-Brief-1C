export default {
    state: {
        on_graph:    'pays',
        graph_color: [],
        
        bar_dataset: null,
        pi_dataset: null,
        
        bar_graph: {},
        pie_graph: {},

        
    },

    mutations: {
        updateGraph: function(state, graph_name){ state.on_graph = graph_name },

        getColors: function(state, nb_colors){},

        setBarGraph:    function(state, graph){ state.bar_graph = graph },
        setBarDatasets: function(state, dataset){ state.bar_dataset =  dataset},
        

        setPieGraph:    function(state, graph){ state.pie_graph = graph },

        // Config bars
        configBarChart: function(state, val){

            return {
                type: 'bar',
                data: state.dataset,
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
                        legend: { display: false, },
                    },

                    scales: {
                        x: { grid: { display: true } },
                        y: { grid: { display: false } }
                    },

                    onClick: this.clickHandler
                },
            };
        },


    }
}