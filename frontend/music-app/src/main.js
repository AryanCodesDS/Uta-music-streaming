import { createApp } from 'vue'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.js'
//import './style.css'
import App from './App.vue'
import router from '../plugins/router.js'
import store from '../plugins/store.js'

createApp(App).use(router).use(store).mount('#app')
