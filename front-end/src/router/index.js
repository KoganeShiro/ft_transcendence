import { createRouter, createWebHistory } from 'vue-router';
import Welcome from '../views/welcome.vue';
import TermsAndConditions from '../views/RGPD/terms_and_conditions.vue';
import PrivacyPolicy from '../views/RGPD/privacy_policy.vue';
import Login from '../views/sign/login.vue';
import Register from '../views/sign/register.vue';
import Logout from '../views/sign/logout.vue';
import Avatar from '../components/atoms/avatar.vue';
import Profile from '../views/profile.vue';
import Play from '../views/game/game_choice.vue'
import Settings from '../views/settings/settings.vue';
import credits from '../views/credits.vue';
import Stats from '../components/profile/Stats.vue';
import History from '../components/profile/History.vue';
import Friends from '../components/profile/Friends.vue';

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
    path: '/logout',
    name: 'Logout',
    component: Logout,
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
  },
  {
    path: '/stats',
    name: 'Stats',
    component: Stats,
  },
  {
    path: '/history',
    name: 'History',
    component: History,
  },
  {
    path: '/friends',
    name: 'Friends',
    component: Friends,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;