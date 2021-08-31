

// Create a Vue application
const app = Vue.createApp({

  delimiters: ['[[', ']]'],
  data() {
    return {
      items: [],
      buffer: {first_name:'',last_name:'',email:'',username:'',is_superuser:false,is_staff:false,is_active:false},
      action: "List",
      error: {},
      userProfile: {id:'',amount:'',start_date:''},
      pagination : { pageItems : [],itemsPerPage : 12, currentPage:1 ,numberOfPages: 0,numberOfItems:0 },
      editIndex:-1,
    }
  },
  mounted() {      
    this.getItemList(); 
   
  },
  computed:{

    update_pagination : function(){
      this.pagination.numberOfItems = this.items.length
      this.pagination.numberOfPages = Math.ceil(this.pagination.numberOfItems / this.pagination.itemsPerPage);
      this.pagination.pageItems = this.items.slice( (this.pagination.currentPage - 1) * this.pagination.itemsPerPage, (this.pagination.currentPage-1)*this.pagination.itemsPerPage + this.pagination.itemsPerPage );
      
    },

  },

  updated(){

    $.fn.datepicker.dates['fr'] = {
      days: ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"],
      daysShort: ["dim.", "lun.", "mar.", "mer.", "jeu.", "ven.", "sam."],
      daysMin: ["d", "l", "ma", "me", "j", "v", "s"],
      months: ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
      monthsShort: ["janv.", "févr.", "mars", "avril", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."],
      today: "Aujourd'hui",
      monthsTitle: "Mois",
      clear: "Effacer",
      weekStart: 1,
    }
    
    //currentDate = new Date( "{{parameter.start_date|date:'Y-m-d' }}" );
    //Date picker
    $('#id_start_date').datepicker({
    autoclose: true,
    format: "01-mm-yyyy",
    viewMode: "months", 
    minViewMode: "months",
    language:'fr',
    })

  },
   
  methods: {

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
        axios.get('/users/api').then(function (response) {
              _this.items = response.data;
        })
      .catch(function (error) { console.log(error);});
    },

    createItem : function(){

      var _this = this;
      data = JSON.stringify(this.buffer);
      axios.post("/users/api/",data,{headers: {'Content-Type': 'application/json','X-CSRFTOKEN': '{{ csrf_token }}'}})
      .then(function(response){
        console.log(response.data);
        //_this.items.push(response.data)
        //_this.items.splice(0,0,response.data);
        _this.items.push(response.data);
        _this.action="List"
      })
      .catch(function(error){
        _this.error = error.response.data;
      })

    },

    updateItem : function(id){

      var _this = this;
      data = JSON.stringify(this.buffer);
      axios.patch("/users/api/"+id+"/",data,{headers: {'Content-Type': 'application/json','X-CSRFTOKEN': '{{ csrf_token }}'}})
      .then(function(response){
        console.log(response.data);
        _this.items[ (_this.pagination.currentPage - 1) *_this.pagination.itemsPerPage + _this.editIndex ]  = response.data;
        _this.action="List"
      })
      .catch(function(error){
        _this.error = error.response.data;
      })

    },

    deleteItem : function(id,index){
      var _this = this
      axios.delete("/users/api/"+id,{headers: {'X-CSRFTOKEN': '{{ csrf_token }}'}})
      .then(function(response){
        //console.log(response);
        //_this.items.splice(index,1);
        _this.items.splice((_this.pagination.currentPage - 1) *_this.pagination.itemsPerPage + index,1);
      })
      .catch(function(error){
        //console.log(error);
      })
    },

    editUserProfile : function(user_id){

        var _this = this;
        axios.get('/userprofiles/api/get_userprofile_by_userid/'+user_id).then(function (response) {
              _this.userProfile = response.data;
              _this.action="UserProfile"
        })
      .catch(function (error) { console.log(error);});

    },
    
    updateUserProfile : function(id){

      var _this = this;
      this.userProfile.start_date = $('#id_start_date').val();
      data = JSON.stringify(this.userProfile);
      axios.patch("/userprofiles/api/"+id+"/",data,{headers: {'Content-Type': 'application/json','X-CSRFTOKEN': '{{ csrf_token }}'}})
      .then(function(response){
        //console.log(response.data);
        _this.action="List";
      })
      .catch(function(error){
        _this.error = error.response.data;
      })

    },

    newItem : function(){
      this.action="Create";
    },

    editItem : function(index){

      this.editIndex = index;
      this.action="Edit";
      let selItem = this.items[(this.pagination.currentPage - 1) *this.pagination.itemsPerPage + index];
      this.buffer = JSON.parse(JSON.stringify(selItem));
    },


    cancelAction : function(){
      this.action="List";
    }

  }


}).mount('#app');
