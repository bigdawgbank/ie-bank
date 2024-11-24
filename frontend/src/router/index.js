import Vue from "vue";
import VueRouter from "vue-router";
import AppAccounts from "../components/AppAccounts.vue";
import Home from "../components/Home.vue";
import Register from "../components/Register.vue";
import Login from "../components/Login.vue";
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
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

// Route guard from Flask API
router.beforeEach(async (to, from, next) => {
  // Check if the route requires authentication
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // Make a simple request to any protected endpoint
    try {
      // This will succeed if we have a valid session cookie
      const response = await authService.checkSession();
      if (response.authenticated) {
        next();
      } else {
        next("/login");
      }
    } catch (error) {
      next("/login"); // Error occurred, redirect to login
    }
  } else {
    next(); // Not a protected route, proceed
  }
});

export default router;
