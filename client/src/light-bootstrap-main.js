// A plugin file where you could register global components used across the app
import GlobalComponents from './globalComponents';
// A plugin file where you could register global directives
import GlobalDirectives from './globalDirectives';
// Sidebar on the right. Used as a local plugin in DashboardLayout.vue
import SideBar from './components/SidebarPlugin';

// asset imports
import 'bootstrap/dist/css/bootstrap.css';
import './assets/sass/light-bootstrap-dashboard.scss';

/**
 * This is where dashboard related plugins are registerd.
 */
export default {
  install(Vue) {
    Vue.use(GlobalComponents);
    Vue.use(GlobalDirectives);
    Vue.use(SideBar);
  },
};
