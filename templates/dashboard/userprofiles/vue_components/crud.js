// Create a Vue application
const app = Vue.createApp({

  delimiters: ['[[', ']]'],
  data() {
    return {
      item: {id:'',montant:'',start_date:''},
      error: {},
    }
  },
  mounted() {      
    this.getItemList(); 
   
  },
   
  methods: {
    getItemList : function(){
        var _this = this;
        axios.get('/userprofiles/api/get_userprofile_by_userid/{{selected_user_id}}').then(function (response) {
              _this.item = response.data;
        })
      .catch(function (error) { console.log(error);});
    },

    updateItem : function(id){

      var _this = this;
      this.item.start_date = $('#id_start_date').val();
      data = JSON.stringify(this.item);
      axios.patch("/userprofiles/api/"+id+"/",data,{headers: {'Content-Type': 'application/json','X-CSRFTOKEN': '{{ csrf_token }}'}})
      .then(function(response){
        console.log(response.data);
      })
      .catch(function(error){
        _this.error = error.response.data;
      })

    }
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