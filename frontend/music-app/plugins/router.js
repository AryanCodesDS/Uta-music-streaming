// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
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

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/about',
        name: 'About',
        component: About
    },
    {
        path: '/user-login',
        name: 'userlogin',
        component: userlogin,
        props:true
    },
    {
        path: '/admin-login',
        name: 'adminlogin',
        component: adminlogin
    },
    {
        path: '/admin-dashboard',
        name: 'admindash',
        component : admindash
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
        props:true
    },
    {
        path: '/all-albums',
        name: 'albums',
        component:allalbums
    },
    {
        path: '/my-playlists',
        name: 'allplaylists',
        component:allplay
    },
    {
        path: '/more-songs',
        name: 'moresongs',
        component: allsongs
    },


]

const router = createRouter({ history: createWebHistory(), routes })
export default router
