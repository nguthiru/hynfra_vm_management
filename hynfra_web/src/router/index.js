import { createRouter, createWebHistory } from "vue-router";
import DashView from "../views/DashboardView.vue";

const routes = [
  {
    path: "/",
    name: "dashboard",
    component: DashView,
    children: [
      {
        path: "",
        name: "vms",
        component: () =>
          import(
            /* webpackChunkName: "vms" */ "../components/dashboard/VmPage.vue"
          ),
        children: [],
      },
      {
        path: "vms/:id",
        name: "vms-detail",
        component: () =>
          import(
            /* webpackChunkName: "vms-detail" */ "../components/dashboard/VmDetailPage.vue"
          ),
      },
      {
        path: "vms/create",
        name: "vms-create",
        component: () =>
          import(
            /* webpackChunkName: "vms-create" */ "../components/dashboard/VmCreatePage.vue"
          ),
      },
      {
        path: "payments",
        name: "payments",
        component: () =>
          import(
            /* webpackChunkName: "payments" */ "../components/dashboard/PaymentPage.vue"
          ),
      },
      {
        path: "invoice/:id",
        name: "invoice-detail",
        component: () =>
          import(
            /* webpackChunkName: "invoice" */ "../components/dashboard/InvoiceDetailPage.vue"
          ),
      },
      {
        path: "account/clients",
        name: "clients",
        component: () =>
          import(
            /* webpackChunkName: "clients" */ "../components/dashboard/ClientsPage.vue"
          ),
      },
    ],
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/auth",
    name: "auth",
    component: () =>
      import(/* webpackChunkName: "auth" */ "../views/AuthView.vue"),
    children: [
      {
        path: "login",
        name: "login",
        component: () =>
          import(
            /* webpackChunkName: "login" */ "../components/auth/LoginPage.vue"
          ),
      },
      {
        path: "register",
        name: "register",
        component: () =>
          import(
            /* webpackChunkName: "register" */ "../components/auth/RegisterPage.vue"
          ),
      },
      {
        path: "sso-login",
        name: "sso",
        component: () =>
          import(
            /* webpackChunkName: "sso" */ "../components/auth/SSOPage.vue"
          ),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
