import { createRouter, createWebHistory } from 'vue-router';
import Welcome from '../views/welcome.vue';
import TermsAndConditions from '../views/RGPD/terms_and_conditions.vue';
import PrivacyPolicy from '../views/RGPD/privacy_policy.vue';
import Login from '../views/sign/login.vue';
import Register from '../views/sign/register.vue';
import Logout from '../views/sign/logout.vue';
import Avatar from '../components/atoms/Avatar.vue';
import Profile from '../views/profile.vue';
import Play from '../views/game/game_choice.vue'
import Settings from '../views/settings/settings.vue';
import credits from '../views/credits.vue';
import Stats from '../components/profile/Stats.vue';
import History from '../components/profile/History.vue';
import Friends from '../components/profile/Friends.vue';
import AddFriend from '../components/profile/AddFriend.vue';
import Account from '../views/settings/account.vue';
import Appearence from '../views/settings/appearence.vue';
import LanguageSwitcher from '../components/settings/LanguageSwitcher.vue';
// import ThemeSwitcher from '../components/settings/ThemeSwitcher.vue';
// import Theme from '../components/settings/Theme.vue';

// import Loose from '../views/game/loose.vue';
// import Win from '../views/game/win.vue';
import GameChoice from '../views/game/game_choice.vue';
import ModeSelection from '../views/game/mode_selection.vue';
import PongFront from '../views/game/pong.vue';
import TicTacToe from '../views/game/tic_tac_toe.vue';
import CreateTournament from '../components/game/CreateTournament.vue';
import waitingPlayers from '../views/game/waiting_players.vue';

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
  },
  {
    path: '/add-friend',
    name: 'AddFriend',
    component: AddFriend,
  },
  {
    path: '/account',
    name: 'Account',
    component: Account,
  },
  {
    path: '/appearence',
    name: 'Appearence',
    component: Appearence,
  },
  {
    path: '/language-switcher',
    name: 'LanguageSwitcher',
    component: LanguageSwitcher,
  },
  {
    path: "/game-choice",
    name: "gameChoice",
    component: GameChoice,
  },
  {
    path: "/select-mode",
    name: "modeSelection",
    component: ModeSelection,
  },
  {
    path: "/pong/:mode",
    name: "PongFront",
    component: PongFront,
  },
  {
    path: "/tic-tac-toe/:mode",
    name: "TicTacToe",
    component: TicTacToe,
  },
  {
    path: "/create-tournament",
    name: "CreateTournament",
    component: CreateTournament,
  },
  {
    path: "/waiting-players",
    name: "waitingPlayers",
    component: waitingPlayers,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;