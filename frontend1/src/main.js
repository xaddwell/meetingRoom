import Vue from 'vue'
import App from './App.vue'
import router from './router'
import iView from 'iview'
import * as echarts from 'echarts'
import 'iview/dist/styles/iview.css'
import moment from 'moment'

import qs from 'qs';
Vue.prototype.qs = qs;

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI);

import './assets/css/reset.css'

import axios from 'axios'
import VueAxios from "vue-axios";
Vue.use(VueAxios, axios)

const BaseUrl='http://121.36.62.187:8888'


Vue.config.productionTip = false
Vue.use(iView);
Vue.prototype.$echarts = echarts;


new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
