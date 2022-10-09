import Vue from 'vue'
import VueRouter from 'vue-router'

import Login from '../components/user/Login.vue'
import Home from '../components/user/Home.vue'
import Approved from '../components/user/history/Approved.vue'
import History from '../components/user/history/History.vue'
import NotApproved from '../components/user/history/NotApproved.vue'
import Approving from '../components/user/history/Approving'
import Book from '../components/user/book/Book.vue'
import CancelBook from '../components/user/book/CancelBook.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: ()=>import('../components/Login')},
  {
    path:'/register', 
    name:'Regiser',
    component: ()=> import('../components/Register')
  },
  {
    path:'/home', 
    name:'home',
    component: ()=> import('../components/Home'),
    redirect: '/meetingRooms',
    children: [
      { path: '/meetingRooms', component: ()=> import('../components/room/Rooms.vue')},
      { path: '/meetingRoomHistory', component: ()=> import('../components/room/RoomHistory.vue')},
      { path: '/department', component: ()=> import('../components/department/Departments.vue')},
      { path: '/depHistory', component: ()=> import('../components/department/DepHistory.vue') },
      { path: '/approved', component: ()=> import('../components/approve/Approved.vue') },
      { path: '/notApproved', component: ()=>import('../components/approve/NotApproved.vue') },
      { path: '/log', component: ()=> import('../components/log/Log.vue')},
      {path: '/deptusers', component: ()=> import('../components/department/Deptuser.vue')}
    ]
  },
  {
	  path:'/user_home',
	  name:'home',
	  component: Home,
	  redirect: '/use_book',
	  children: [
	    { path: '/user_approved', component: Approved },
		{ path: '/user_meetingStatisticHistory', component: ()=> import('../components/room/meetingStatisticHistory')},
	    { path: '/user_history', component: History },
	    { path: '/user_notApproved', component: NotApproved },
	    { path: '/user_approving', component: Approving },
	    { path: '/user_book', component: Book },
	    { path: '/user_cancelBook', component: CancelBook },
	    { path: '/user_home', component: Home }
	  ]
  },
  {
    path:'/test', 
    name:'test',
    component: ()=> import('../components/test')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})
// 挂载路由导航守卫
router.beforeEach((to, from, next) => {
  // to 表示将要访问的路径
  // from 表示从哪个路径跳转而来
  // next 是一个函数，表示放行
  // next() 直接放行 next('/login') 强制跳转
  if (to.path === '/login') return next();
  if (to.path === '/register') return next();
  // 获取token
  const tokenStr = window.sessionStorage.getItem('username');
  if (!tokenStr) return next('/login')
  next()
})
export default router
