// Create a Vue application
const stats = Vue.createApp({})


stats.component('stats', {
  delimiters: ['[[', ']]'],
  data() {
    return {
      items: [],
    }
  },

  props : ['block1','block2', 'block3','block4'],
  template: `{% include  "./form.html" %}`,

  mounted() {      

     this.getItemList()
   
  },
   
  methods: {

    getItemList : function(){
      var _this = this;
      axios.get('/operations/api/get_global_stats/').then(function (response) {
            console.log(response.data)
            _this.block1.title="hhhhh";
      })
    .catch(function (error) { console.log(error);});
    }


  }
})

stats.mount('#stats')
