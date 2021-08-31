// Create a Vue application
const spinner = Vue.createApp({})


spinner.component('square-spinner', {
  delimiters: ['[[', ']]'],
  data() {
    return {
        isLoading: this.loading,
        styles: {
          backgroundColor: this.color,
          width: this.width + 'px',
          height: this.height + 'px'
        }
    }
  },

  props : {
    loading: {
      type: Boolean,
      default: true
    },
    color: {
      type: String,
      default: '#333',
    },
    width: {
      type: String,
      default: '40',
    },
    height: {
      type: String,
      default: '40',
    }
  },
  template: `{% include  "./template.html" %}`,

})

spinner.mount('#spinner')
