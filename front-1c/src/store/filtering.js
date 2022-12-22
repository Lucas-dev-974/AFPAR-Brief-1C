import request from '../services/fetch.js'

export default {
    state: {
        items_select: {
            items: [],
            model: []
        },

        nb_items: 6,
        
        year_select: {
            years: [],
            model: 'Toutes'
        },

        pays_select: {
            model: null,
            pays:  null
        }
    },

    mutations: {
        setYearsItems:   function(state, values){ state.year_select.years = values },
        yearUpdateModel: function(state, value){ state.year_select.model = value },

        paysUpdateModel: function(state, value){ state.pays_select.model = value },
        nbItemUpdate:    function(state, value){ state.nb_items = value },        
    },

    actions: {
        getYears: async function({ commit, state }){
            const response = await request.get('/api/years')
            state.year_select.years = response.years
        },

        getPays: async function({commit, state}){
            const response = await request.get('/api/pays')
            state.pays_select.pays = response
        }
    }
}