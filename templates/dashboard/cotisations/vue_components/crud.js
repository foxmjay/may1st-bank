// Create a Vue application
const app = Vue.createApp({

  delimiters: ['[[', ']]'],
  data() {
    return {
      items: [],
      error: {},
      pagination : { pageItems : [],itemsPerPage : 12, currentPage:1 ,numberOfPages: 0,numberOfItems:0 },
    }
  },
  mounted() {      
    this.getItemList(); 
  },
   
  computed:{

    update_pagination : function(){

      this.pagination.numberOfItems = this.items.length
      this.pagination.numberOfPages = Math.ceil(this.pagination.numberOfItems / this.pagination.itemsPerPage);
      this.pagination.pageItems = this.items.slice( (this.pagination.currentPage-1)*this.pagination.itemsPerPage  ,this.pagination.currentPage*this.pagination.itemsPerPage);

    },

  },
  methods: {
    formatDate(date){
      
      return moment(date,'YYYY-MM-DD').locale('fr').format('LL');
    },

    checkDate : function(index){
      
      cotDate = new Date(this.pagination.pageItems[index].date);
      now = new Date();
      return cotDate < now
    },

    nextPage : function(){
      if (this.pagination.currentPage < this.pagination.numberOfPages){
        this.pagination.currentPage+=1;
      }
    },

    previousPage : function(){
      if(this.pagination.currentPage > 1){
        this.pagination.currentPage-=1;
      }
    },

    getItemList : function(){
        var _this = this;
        axios.get('/cotisations/api/get_cotisations/{{selected_user_id}}').then(function (response) {
              _this.items = response.data;
               var numberOfPages = Math.ceil(response.data.length / _this.pagination.itemsPerPage);
              _this.pagination.currentPage = numberOfPages;

        })
      .catch(function (error) { console.log(error);});
    },

    createItem : function(index){

      var _this = this;
      data = JSON.stringify({user:"{{ selected_user_id }}",month:_this.pagination.pageItems[index].date});
      axios.post("/cotisations/api/",data,{headers: {'Content-Type': 'application/json','X-CSRFTOKEN': '{{ csrf_token }}'}})
      .then(function(response){
        _this.items[ (_this.pagination.currentPage - 1) *_this.pagination.itemsPerPage + index ]  = response.data;
      })
      .catch(function(error){
        _this.error = error.response.data;
      })

    },

    deleteItem : function(id,index){
      var _this = this
      axios.delete("/cotisations/api/"+id,{headers: {'X-CSRFTOKEN': '{{ csrf_token }}'}})
      .then(function(response){
        _this.items[(_this.pagination.currentPage - 1) *_this.pagination.itemsPerPage + index].cotisation = null;
      })
      .catch(function(error){
        console.log(error);
      })
    },
  }


}).mount('#app');

