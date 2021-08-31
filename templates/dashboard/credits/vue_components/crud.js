// Create a Vue application
const app = Vue.createApp({

  delimiters: ['[[', ']]'],
  data() {
    return {
      items: [],
      buffer: {user:'',amount:'',start_date:'',end_date:'',cotisation_amount:'',months:'',status:'inprogress'},
      action: "List",
      error: {},
      users : [],
      status: [],
      editIndex:-1,
      pagination : { pageItems : [],itemsPerPage : 12,currentPage:1,numberOfPages: 0,numberOfItems:0 },
      selected_user_id : "{{ selected_user_id }}",
      isLoading: true,

    }
  },

  mounted() {      
    this.getUserList();
    this.getCreditStatus();
    this.getItemList();
    

  },
  computed: {

    calculate : function(){
      
      //this.buffer.start_date = $('#id_start_date').val();

      if(!this.buffer.start_date){
        this.buffer.start_date = moment().format('DD-MM-YYYY')
      }

      if(this.buffer.months)
        this.buffer.cotisation_amount = (this.buffer.amount / this.buffer.months).toFixed(2)

      startDate = moment(this.buffer.start_date,'DD-MM-YYYY',true);
      startDate.add(this.buffer.months,'months')
      this.buffer.end_date=moment(startDate).format("DD-MM-YYYY");
    },

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
    });
    var _this = this
     $('#id_start_date').on('change',function(){
         _this.buffer.start_date = $('#id_start_date').val();
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

        var url = '/credits/api'
        if (this.selected_user_id !='None')
          url = url+'/get_credits_by_user/'+this.selected_user_id
        axios.get(url).then(function (response) {
              _this.items = response.data;
              _this.isLoading=false;
        })
      .catch(function (error) { console.log(error);});
    },

    getUserList : function(){
      var _this = this;
      axios.get('/users/api').then(function (response) {
            _this.users = response.data;
      })
    .catch(function (error) { console.log(error);});
    },

    getCreditStatus : function(){
      var _this = this;
      axios.get('/credits/api/get_credit_status').then(function (response) {
            _this.status = response.data
      })
    .catch(function (error) { console.log(error);});
    },

    statusLabel: function(key){

      return this.status.filter( 
          function(m){
              return m[0] === key;
          })[0][1];
    },

    createItem : function(){

      var _this = this;
      data = JSON.stringify(this.buffer);
      axios.post("/credits/api/",data,{headers: {'Content-Type': 'application/json','X-CSRFTOKEN': '{{ csrf_token }}'}})
      .then(function(response){
        _this.items.push(response.data);
        _this.action="List"
      })
      .catch(function(error){
        console.log(error);
        _this.error = error.response.data;
      })

    },

    updateItem : function(id){

      var _this = this;
      data = JSON.stringify(this.buffer);
      axios.patch("/credits/api/"+id+"/",data,{headers: {'Content-Type': 'application/json','X-CSRFTOKEN': '{{ csrf_token }}'}})
      .then(function(response){
         _this.items[ (_this.pagination.currentPage - 1) *_this.pagination.itemsPerPage + _this.editIndex ]  = response.data;
         _this.editIndex=-1;
        _this.action="List";
        _this.buffer={user:'',amount:'',start_date:'',end_date:'',cotisation_amount:'',months:'',status:'inprogress'};
      })
      .catch(function(error){
        _this.error = error.response.data;
      })

    },

    deleteItem : function(id,index){
      var _this = this
      axios.delete("/credits/api/"+id,{headers: {'X-CSRFTOKEN': '{{ csrf_token }}'}})
      .then(function(response){
        //console.log(response);
        _this.items.splice((_this.pagination.currentPage - 1) *_this.pagination.itemsPerPage + index,1);
      })
      .catch(function(error){
        //console.log(error);
      })
    },


    newItem : function(){
      if(this.selected_user_id != 'None'){
        this.buffer.user = this.selected_user_id;
      }
      this.action="Create";
    },

    editItem : function(index){
      this.editIndex = index;
      this.action="Edit";
      let selItem = this.items[(this.pagination.currentPage - 1) *this.pagination.itemsPerPage + index];
      this.buffer = JSON.parse(JSON.stringify(selItem));
      //console.log(this.buffer);
      this.buffer.user=this.buffer.user.id;

    },

    cancelAction : function(){
      this.action="List";
      this.buffer={user:'',amount:'',start_date:'',end_date:'',cotisation_amount:'',months:'',status:'inprogress'}
    }

  }


});

app.mount('#app');
