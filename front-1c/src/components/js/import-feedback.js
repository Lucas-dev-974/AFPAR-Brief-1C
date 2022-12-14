import request from '../../services/fetch.js'


export default{
    data(){
        return{
            csv_file: null,
        }
    },

    mounted(){
        this.getImportLog()
    },

    methods: {
        getImportLog: async function(){
            const feedack_container  = document.getElementById('feedback_container')
            
            const response = await request.get('/api/csv/import/log')
            console.log(response);
            if(!response){
                feedack_container.innerHTML = 'Aucun import '
            }else{
                const lst_import_date = new Date(response.date_import)
                const file_name_field = document.createElement('p')
                file_name_field.innerText = 'Dernier fichier importer: '  + response.file_name + ', date d\'import: ' + lst_import_date.getMonth() + '/' + lst_import_date.getDay() + '/' + lst_import_date.getFullYear()
                

                this.renderFeedback(response.log)

                feedack_container.appendChild(file_name_field)
            }
                
        },

        importCSV: async function(){
            const form_data = new FormData()
            form_data.append('csv_file', this.csv_file)
            const response = await request.post('/api/csv/import', form_data)
            
            if(!response) return false

            console.log(response);
            this.renderFeedback(response.status)

        },

        openFile: function(){
            var input = document.createElement('input')
            input.style.visibility = 'hidden';
            input.type = 'file'

            input.onchange = e => { 
                this.csv_file = e.target.files[0]; 
                this.importCSV()
             }

            input.click();
        },

        renderFeedback: function(status){
            const feedack_container  = document.getElementById('feedback_container')
            feedack_container.innerHTML = ''
            
            const inserted_container = document.createElement('div')
            const failed_container   = document.createElement('div')
            const repearable_container = document.createElement('div')

            failed_container.setAttribute('class', 'd-flex justify-space-between')

            if(status.rows_inserted){
                const text = document.createElement('p')
                
                text.innerText = status.rows_inserted + ' import effectuer'

                inserted_container.appendChild(text)
                feedack_container.appendChild(inserted_container)
            }   

            if(status.rows_irreparable){
                const text = document.createElement('p')

                const buttons_group   = document.createElement('div')
                buttons_group.setAttribute('class', 'd-flex')

                const download_button = document.createElement('a')
                const delete_button   = document.createElement('button')

                download_button.innerText = 'télécharger'
                download_button.setAttribute('class', 'px-2')
                download_button.href = this.$store.state.backend_host + '/api/csv/fails/download'

                delete_button.innerText   = 'supprimer'
                delete_button.setAttribute('class', 'px-2')
                delete_button.onclick = this.deleteFailed
                
                text.innerText = status.rows_irreparable + ' import deffectueux & irreparables !'
                failed_container.appendChild(text)
                feedack_container.appendChild(failed_container)

                buttons_group.appendChild(download_button)
                buttons_group.appendChild(delete_button)
                failed_container.appendChild(buttons_group)
            }
        },

        deleteFailed: function(){
            console.log('delte');
        },
    }
}