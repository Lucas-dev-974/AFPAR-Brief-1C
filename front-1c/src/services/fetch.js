import store from "../store/index.js"
const queryString = require('query-string');

export default {
    host: store.state.backend_host,

    default_options(method, params){
        let token = store.state.token ?? ''
        let parameters = JSON.stringify(params)
        let Authorization = {}
        let head = {}

        if(params instanceof FormData){
            parameters = { body: params }
        }else{
            head = {
                'Accept':       'application/json',
                'Content-Type': 'application/json',
            }
            if(method == 'GET')
                parameters = { query: {...params} }
            else
                parameters = { body: JSON.stringify(params) }

        }

        if(token && token != '') Authorization = {'Authorization':`Token ${token}`}
        
        return {    
            method: method,
            headers: {
                ...head,
                ...Authorization,
            },
            ...parameters,
        }
    },

    async post(uri, params){
        const request = await window.fetch(this.host + uri, this.default_options('POST', params))
        return await this.getResponse(request)
    },

    async get(uri, params){
        const request = await window.fetch(this.host + uri + this.stringifyParser(params), this.default_options('GET', params))
        return await this.getResponse(request)
    },

    async delete(uri, params){
        const request = await fetch(this.host + uri, this.default_options('DELETE', params))
        return await this.getResponse(request)
    },


    async getResponse(_request){
        const json = await _request.json()
        if(json.error || json.errors || _request.status == 401){
            let error_message = json.error || json.errors || json.detail

            store.commit('Notif', {
                on: true,
                color: 'warning',
                message: error_message
            })
            
            return false
        }

        if(_request.status != 200) return false

        return json
    },

    /**
     * Transform Json object {regions: ["France", "United Kingdom", ...]} to url query parameters "?regions=France,United Kingdom,..."
     * 
     * @param json params 
     * @returns string url parameters
     */
    stringifyParser:function(params){
        let str = ''
        
        if(params != undefined){
            str = '?'
            const size = Object.keys(params).length

            for(let i = 0; i < size; i++){
                str += Object.keys(params)[i] + '='
                str += Object.values(params)[i] + '&'
            } 
        }
        return str
    }
}