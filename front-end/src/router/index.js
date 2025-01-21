import { createRouter, createWebHistory } from 'vue-router';
import Welcome from '../views/welcome.vue';
import TermsAndConditions from '../views/terms_and_conditions.vue';

const routes = [
  {
    path: '/',
    name: 'welcome',
    component: Welcome,
  },
  {
    path: '/terms',
    name: 'TermsAndConditions',
    component: TermsAndConditions,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;