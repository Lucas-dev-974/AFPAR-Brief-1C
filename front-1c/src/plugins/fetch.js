import store from "../store/index.js"

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
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
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
        const request = await window.fetch(this.host + uri, this.default_options('GET', params))
        return await this.getResponse(request)
    },

    async delete(uri, params){
        const request = await fetch(this.host + uri, this.default_options('DELETE', params))
        return await this.getResponse(request)
    },


    async getResponse(_request){
        const json = await _request.json()
        if(json.error || json.errors){
            let error_message = json.error || json.errors

            store.commit('Notif', {
                on: true,
                color: 'warning',
                message: error_message
            })
            
            return false
        }

        if(_request.status != 200) return false

        return json
    }

}