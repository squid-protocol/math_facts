import { createRouter, createWebHistory } from 'vue-router'
import GameView from './views/GameView.vue'

const routes = [
  {
    path: '/',
    name: 'Practice',
    component: GameView
  },
  {
    path: '/analytics/',
    name: 'Analytics',
    component: () => import('./views/AnalyticsView.vue')
  },
  {
    path: '/about/',
    name: 'About',
    component: () => import('./views/AboutView.vue')
  },
  {
    path: '/faq/',
    name: 'Faq',
    component: () => import('./views/FaqView.vue')
  },
  {
    path: '/privacy-policy/',
    name: 'Privacy',
    component: () => import('./views/PrivacyView.vue')
  },
  {
    path: '/terms/',
    name: 'Terms',
    component: () => import('./views/TermsView.vue')
  }
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

export default router