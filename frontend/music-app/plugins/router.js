// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import store from './store'
import Home from '../src/components/Home.vue'
import Songpage from '../src/components/Songpage.vue'
import About from '../src/components/About.vue'
import userlogin from '../src/components/userlogin.vue'
import usersignup from '../src/components/usersignup.vue'
import adminlogin from '../src/components/adminlogin.vue'
import admindash from '../src/components/Admindash.vue'
import allsongs from '../src/components/allsongs.vue'
import allalbums from '../src/components/allalbums.vue'
import allplay from '../src/components/allplay.vue'
import profile from '../src/components/Profile.vue'
import creator from '../src/components/Creator.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: {
            requiresAuth: false,
        },
    },
    {
        path: '/about',
        name: 'About',
        component: About,
        meta: {
            requiresAuth: false,
          },
    },
    {
        path: '/user-login',
        name: 'userlogin',
        component: userlogin,
        props:true,
        meta: {
            requiresAuth: false,
          },
    },
    {
        path: '/admin-login',
        name: 'adminlogin',
        component: adminlogin,
        meta: {
            requiresAuth: true,
          },
    },
    {
        path:'/profile',
        name:'profile',
        component: profile,
        meta: {
            requiresAuth: true,
          },
    },
    {
        path:'/creator',
        name:'creator',
        component:creator,
        meta: {
            requiresAuth: true,
          },
    },
    {
        path: '/admin-dashboard',
        name: 'admindash',
        component : admindash,
        //beforeEnter: (to, from) => {
        //    if(store.state.roles.includes("Admin"))
        //   return true
        //}
        meta: {
            requiresAuth: true,
          },
    },
    {
        path: '/user-signup',
        name: 'usersignup',
        component: usersignup
    },
    {
        path: '/all-songs',
        name: 'songs',
        component: Songpage,
        props:true,
        meta: {
            requiresAuth: true,
          },
    },
    {
        path: '/all-albums',
        name: 'albums',
        component:allalbums,
        meta: {
            requiresAuth: true,
          },
    },
    {
        path: '/my-playlists',
        name: 'allplaylists',
        component:allplay,
        meta: {
            requiresAuth: true,
          },
    },
    {
        path: '/more-songs',
        name: 'moresongs',
        component: allsongs,
        meta: {
            requiresAuth: true,
          },
    },


]

const router = createRouter({ history: createWebHistory(), routes })
router.beforeEach((to, from, next) => {
    console.log('Navigating to:', to.name);
    console.log('Requires Authentication:', to.meta.requiresAuth);
    console.log(store.getters.isAuthenticated)
    if (to.meta.requiresAuth && store.getters.isAuthenticated == false) {
        next('/user-login');
    } else {
      next();
    }
  })
export default router
