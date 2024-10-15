import Vue from "vue";
import VueRouter from "vue-router";
import AppAccounts from "../components/AppAccounts.vue";
import Home from "../components/Home.vue";

Vue.use(VueRouter);

// Defining routes
const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/accounts",
    name: "AppAccounts",
    component: AppAccounts,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
