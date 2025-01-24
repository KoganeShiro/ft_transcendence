import { createRouter, createWebHistory } from 'vue-router';
import Welcome from '../views/welcome.vue';
import TermsAndConditions from '../views/terms_and_conditions.vue';
import PrivacyPolicy from '../views/privacy_policy.vue';
import Login from '../views/login.vue';
import Register from '../views/register.vue';
import Avatar from '../components/atoms/avatar.vue';
import Profile from '../views/profile.vue';
import Play from '../views/game/game_choice.vue'
import Settings from '../views/settings/settings.vue';
// import Logout from '../components/sign/logout.vue';
import credits from '../views/credits.vue';

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
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/avatar',
    name: 'Avatar',
    component: Avatar,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
  },
  {
    path: '/play',
    name: 'Play',
    component: Play,
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
  },
  {
    path: '/credits',
    name: 'Credits',
    component: credits,
  },
  {
    path: '/game-choice',
    name: 'GameChoice',
    component: Play,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;