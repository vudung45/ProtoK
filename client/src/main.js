import Vue from 'vue';
import VueRouter from 'vue-router';
import BootstrapVue from 'bootstrap-vue';

import App from './App.vue';
import routes from './routes/routes';

// LightBootstrap plugin
import LightBootstrap from './light-bootstrap-main';

Vue.use(BootstrapVue);
Vue.use(LightBootstrap);
Vue.use(VueRouter);

Vue.config.productionTip = false;

const router = new VueRouter({
  routes,
  linkActiveClass: 'nav-item active',
  scrollBehavior: (to) => {
    if (to.hash) {
      return { selector: to.hash };
    }
    return { x: 0, y: 0 };
  },
  mode: 'history',
  base: process.env.BASE_URL,
});

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
