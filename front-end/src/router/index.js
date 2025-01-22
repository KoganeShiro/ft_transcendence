import { createRouter, createWebHistory } from 'vue-router';
import Welcome from '../views/welcome.vue';
import TermsAndConditions from '../views/terms_and_conditions.vue';
import PrivacyPolicy from '../views/privacy_policy.vue';
import BurgerMenu from '../components/header/burger_menu.vue';
import Login from '../views/login.vue';
import Register from '../views/register.vue';

const routes = [
  {
    path: '/',
    name: 'welcome',
    component: Welcome,
  },
  {
    path: '/privacy',
    name: 'PrivacyPolicy',
    component: PrivacyPolicy,
  },
  {
    path: '/terms',
    name: 'TermsAndConditions',
    component: TermsAndConditions,
  },
  {
    path: '/menu',
    name: 'BurgerMenu',
    component: BurgerMenu,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;