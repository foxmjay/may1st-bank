// Create a Vue application
const app = Vue.createApp({

  delimiters: ['[[', ']]'],
  data() {
    return {
      items: [],
      //item: {first_name:'',last_name:'',email:'',username:'',is_superuser:false,is_staff:false,is_active:false},
    }
  },
  mounted() {      
    this.getItemList(); 
   
  },
   
  methods: {
    getItemList : function(){
        var _this = this;
        axios.get('/operations/api').then(function (response) {
              _this.items = response.data;
        })
      .catch(function (error) { console.log(error);});
    },

  }


}).mount('#app');

