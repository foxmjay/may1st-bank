// Create a Vue application
const app = Vue.createApp({

  delimiters: ['[[', ']]'],
  data() {
    return {
      item: {id:'',cotisation_amount:'',start_date:''},
      error: {},
    }
  },
  mounted() {      
    this.getItemList(); 
   
  },
   
  methods: {
    getItemList : function(){
        var _this = this;
        axios.get('/parameters/api').then(function (response) {
              _this.item = response.data[0];
        })
      .catch(function (error) { console.log(error);});
    },

    initialize : function(){

      var _this = this;
      this.item = { start_date:'{% now "Y-m-d" %}', cotisation_amount:500}; 
      data = JSON.stringify(this.item);
      axios.post("/parameters/api/",data,{headers: {'Content-Type': 'application/json','X-CSRFTOKEN': '{{ csrf_token }}'}})
      .then(function(response){
        _this.item = response.data;
      })
      .catch(function(error){
      })

    },

    updateItem : function(id){

      var _this = this;
      this.item.start_date = $('#id_start_date').val();
      data = JSON.stringify(this.item);      
      axios.patch("/parameters/api/"+id+"/",data,{headers: {'Content-Type': 'application/json','X-CSRFTOKEN': '{{ csrf_token }}'}})
      .then(function(response){
        _this.item = response.data;
        _this.error = {}
      })
      .catch(function(error){
        _this.error = error.response.data;
      })

    },

  }


}).mount('#app');




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
//.datepicker('update', currentDate);