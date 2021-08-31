// Create a Vue application
const stats = Vue.createApp({

  delimiters: ['[[', ']]'],
  data() {
    return {
      items:[],
      theme: [
          {class:'bg-aqua',icon:'fa-money'},
          {class:'bg-green',icon:'fa-bank'},
          {class:'bg-yellow',icon:'fa-money'},
          {class:'bg-red',icon:'fa-bank'}
        ] 
      
    }
  },

  mounted() {      

     this.getItemList()
   
  },
   
  methods: {

    getItemList : function(){
      var _this = this;
      axios.get('/operations/api/get_global_stats/').then(function (response) {
            _this.items=response.data;
      })
    .catch(function (error) { console.log(error);});
    }


  }

})

stats.mount('#stats')
