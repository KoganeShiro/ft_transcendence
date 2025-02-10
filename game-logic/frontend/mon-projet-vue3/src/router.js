import { createWebHistory, createRouter } from 'vue-router'

import ChatComponent from './components/ChatComponent.vue'
import PongGame from './components/PongGame.vue'
import PongGameVersus from './components/PongVersus.vue'

const routes = [
  { path: '/chat', component: ChatComponent },
  { path: '/pong', component: PongGame },
  { path: '/versus', component:PongGameVersus}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router