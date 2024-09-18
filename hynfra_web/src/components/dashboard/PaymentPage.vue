<template>
  <div class="container mx-auto p-8">
    <h1 class="text-2xl font-semibold mb-6">Subscription & Billing</h1>

    <div class="mb-6">
      <ul class="flex border-b">
        <li class="mr-1" v-for="tab in tabs" :key="tab.id">
          <a
            class="bg-white inline-block py-2 px-4 text-sm text-blue-500 hover:text-blue-800 font-semibold"
            :class="{
              'border-l border-t border-r rounded-t text-blue-700':
                currentTab === tab.id,
            }"
            @click="currentTab = tab.id"
            href="#"
          >
            {{ tab.name }}
          </a>
        </li>
      </ul>
    </div>

    <div v-if="currentTab === 'rate-plans'" class="rounded-lg p-6">
      <h2 class="text-xl font-semibold mb-4">Rate Plans</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div
          v-for="plan in ratePlans"
          :key="plan.id"
          class="border rounded-lg p-4 text-center transition-all bg-white shadow-sm"
          :class="[
            currentPlan === plan.id
              ? 'bg-blue-500 scale-105'
              : 'border-gray-200',
          ]"
          :style="{
            backgroundColor: currentPlan == plan.id ? plan.color : 'white',
          }"
        >
          <h3 class="text-x font-bold mb-2">{{ plan.name }}</h3>
          <p class="text-gray-600 text-xs mb-4">Up to {{ plan.max_vms }} VMs</p>
          <p class="text-gray-600 text-xs mb-4">
            Up to {{ plan.max_backups }} Backups
          </p>
          <p class="text-xl font-bold mb-4">${{ plan.price }}/mo</p>
          <button
            :class="[
              'primary-button',
              currentPlan === plan.id ? 'opacity-50 cursor-not-allowed' : '',
            ]"
            @click="upgradePlan(plan)"
          >
            {{ currentPlan === plan.id ? "Current Plan" : "Upgrade" }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="currentTab === 'invoices'" class="rounded-lg p-6">
      <h2 class="text-xl font-semibold mb-4">Invoices</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="invoice in invoices"
          :key="invoice.id"
          class="border rounded-lg p-4 cursor-pointer bg-white"
        >
          <RouterLink
            :to="{ name: 'invoice-detail', params: { id: invoice.id } }"
          >
            <div class="flex justify-between items-center mb-2">
              <span class="font-semibold">Invoice #{{ invoice.id }}</span>
              <span
                class="rounded-md text-xs px-2 py-2 font-semibold"
                :class="
                  invoice.is_paid
                    ? 'text-green-500 bg-green-50'
                    : 'text-yellow-500 bg-yellow-50'
                "
              >
                {{ invoice.is_paid ? "Paid" : "Pending" }}
              </span>
            </div>
            <p class="text-gray-600">{{ invoice.date }}</p>
            <p class="text-xl font-bold mt-2">${{ invoice.amount }}</p>
            <div class="flex justify-between items-center mt-4">
              <button class="text-sm text-blue-500 hover:text-blue-700">
                View Details
              </button>
              <button
                class="primary-button text-xs px-6"
                v-if="!invoice.is_paid"
              >
                Pay
              </button>
            </div>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useToast } from "vue-toastification";

var currentTab = ref("rate-plans");
var currentPlan = ref("silver");
var toast = useToast();
var tabs = ref([
  { id: "rate-plans", name: "Rate Plans" },
  { id: "invoices", name: "Invoices" },
]);
var url = process.env.VUE_APP_BASE_URL;

var ratePlans = ref([]);
var invoices = ref([]);

const upgradePlan = async (plan) => {
  currentPlan.value = plan;

  try {
    await axios.post(
      `${url}/payment/rate-plan/${plan.id}/upgrade/`,
      {},
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    toast.success("Plan upgraded successfully");
  } catch (error) {
    if (error.response) {
      if (error.response.data) {
        toast.error(error.response.data.detail);
      }
      return;
    } else {
      toast.error("Failed to upgrade plan");
      console.log(error);
    }
  }
};
const fetchPlans = async () => {
  try {
    var response = await axios.get(`${url}/payment/rate-plan/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    ratePlans.value = response.data["results"];
  } catch (error) {
    if (error.response) {
      if (error.response.data) {
        toast.error(error.response.data.detail);
      }
    } else {
      toast.error("Failed to fetch rate plans");
    }
    console.log(error);
  }
};

const fetchInvoices = async () => {
  try {
    var response = await axios.get(`${url}/payment/invoice/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    invoices.value = response.data["results"];
  } catch (error) {
    if (error.response) {
      if (error.response.data) {
        toast.error(error.response.data.detail);
      }
    } else {
      toast.error("Failed to fetch invoices");
    }
    console.log(error);
  }
};

onMounted(() => {
  fetchPlans();
  fetchInvoices();
});
</script>
