import Vue from 'vue';
import VueRouter from 'vue-router';

import DashboardLayout from '../layout/DashboardLayout.vue';
import Overview from '../pages/Overview.vue';
import Manage from '../pages/Manage.vue';


Vue.use(VueRouter);

const routes = [

  {
    path: '/',
    redirect: '/home',
    component: DashboardLayout,
    children: [
      {
        path: 'home',
        name: 'Home',
        component: Overview,
      },
      {
        path: '/manage',
        name: 'Manage',
        component: Manage,
      },
    ],
  },
  { path: '*', redirect: '/home' },
];

export default routes;
