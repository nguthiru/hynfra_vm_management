<template>
  <div class="max-w-3xl mx-auto p-6">
    <!-- Invoice Header -->
    <div class="flex justify-between items-center mb-12">
      <h1 class="text-2xl font-bold text-gray-900">
        Invoice #{{ invoice.id }}
      </h1>
      <div
        :class="invoiceStatusClass"
        class="px-6 py-2 rounded-full text-sm font-semibold"
      >
        {{ invoice.is_paid ? "Paid" : "Pending" }}
      </div>
    </div>

    <!-- Invoice Meta -->
    <div class="bg-white shadow-2xl rounded-xl p-8 mb-12">
      <div class="flex justify-between">
        <div class="space-y-2">
          <p class="text-sm text-gray-400">Invoice Date</p>
          <p class="font-semibold text-lg text-gray-800">
            {{ formatDate(invoice.created_at) }}
          </p>
        </div>
        <div class="space-y-2">
          <p class="text-sm text-gray-400">Due Date</p>
          <p class="font-semibold text-lg text-gray-800">
            {{ formatDate(invoice.due_date) }}
          </p>
        </div>
        <div v-if="invoice.status === 'Paid'" class="space-y-2">
          <p class="text-sm text-gray-400">Payment Date</p>
          <p class="font-semibold text-lg text-gray-800">
            {{ formatDate(invoice.paymentDate) }}
          </p>
        </div>
      </div>
    </div>

    <!-- Invoice Items Table -->
    <div class="bg-white shadow-2xl rounded-xl p-8">
      <table class="w-full text-left">
        <thead class="text-sm text-gray-400 uppercase border-b">
          <tr>
            <th class="pb-4">Item</th>
            <th class="pb-4">Date</th>
            <th class="pb-4">Total</th>
          </tr>
        </thead>
        <tbody class="text-gray-600">
          <tr
            v-for="item in invoice.items"
            :key="item.id"
            class="border-b last:border-b-0"
          >
            <td class="py-4">{{ item.name }}</td>
            <td class="py-4">{{ formatDate(item.created_at) }}</td>
            <td class="py-4 font-semibold">
              {{ formatCurrency(item.amount) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Payment Button or Payment Info -->
    <div class="mt-12 text-center">
      <button
        v-if="!invoice.is_paid"
        @click="payInvoice"
        class="flex items-center mx-auto bg-indigo-500 hover:bg-indigo-600 text-white px-10 py-4 rounded-full text-lg shadow-lg transition-all ease-in-out duration-300"
      >
        <spring-spinner v-if="paymentLoading" size="22" class="mx-auto" />

        <div class="container" v-else>
          Pay Now
          <vue-feather type="credit-card" class="inline-block ml-3" />
        </div>
      </button>

      <div v-else class="flex items-center justify-center space-x-3 mt-6">
        <vue-feather type="check-circle" class="text-green-500" />
        <p class="text-lg font-semibold text-green-600">
          This invoice was paid on {{ formatDate(invoice.updated_at) }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useToast } from "vue-toastification";
import { SpringSpinner } from "epic-spinners";
var url = process.env.VUE_APP_BASE_URL;
const paymentLoading = ref(false);
var toast = useToast();
const route = useRoute();
const invoice = ref({
  id: "INV-12345",
  date: "2024-09-12",
  dueDate: "2024-10-12",
  paymentDate: null, // Or a date if paid
  status: "Unpaid", // or 'Paid'
  items: [
    {
      id: 1,
      name: "Web Development",
      quantity: 1,
      unitPrice: 500,
      total: 500,
    },
    {
      id: 2,
      name: "Hosting (1 Year)",
      quantity: 1,
      unitPrice: 100,
      total: 100,
    },
  ],
});
const formatCurrency = (amount) => {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount);
};
const formatDate = (date) => {
  const options = { year: "numeric", month: "long", day: "numeric" };
  return new Date(date).toLocaleDateString(undefined, options);
};
const payInvoice = async () => {
  try {
    paymentLoading.value = true;
    await axios.post(
      `${url}/payment/invoice/pay/`,
      {
        invoices: [route.params["id"]],
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    toast.success("Invoice paid successfully");
    getInvoiceDetails();
  } catch (error) {
    if (error.response) {
      if (error.response.data) {
        toast.error(error.response.data.detail);
      }
    } else {
      console.error(error);
      toast.error("Failed to pay invoice");
    }
  } finally {
    paymentLoading.value = false;
  }
};
const invoiceStatusClass = computed(() => {
  return invoice.value.is_paid
    ? "bg-green-100 text-green-800"
    : "bg-red-100 text-red-800";
});

const getInvoiceDetails = async () => {
  try {
    const response = await axios.get(
      `${url}/payment/invoice/${route.params["id"]}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    console.log(response);
    invoice.value = response.data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  getInvoiceDetails();
});
</script>
