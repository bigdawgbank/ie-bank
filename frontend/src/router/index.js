import Vue from "vue";
import VueRouter from "vue-router";
import AppAccounts from "../components/AppAccounts.vue";
import Admin from "../components/Admin.vue";
import Home from "../components/Home.vue";
import Register from "../components/Register.vue";
import Login from "../components/Login.vue";
import Transfer from "../components/Transfer.vue";
import { authService } from "@/api";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/accounts",
    name: "AppAccounts",
    component: AppAccounts,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin",
    name: "Admin",
    component: Admin,
    meta: { requiresAuth: true },
  },
  {
    path: "/transfer",
    name: "Transfer",
    component: Transfer,
    meta: { requiresAuth: true },
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

// Route guard from Flask API
router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (authService.checkSession()) {
      next();
    } else {
      next("/login");
    }
  } else {
    next();
  }
});

export default router;
