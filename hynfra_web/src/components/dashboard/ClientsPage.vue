<template>
  <div class="max-w-6xl mx-auto p-4">
    <!-- Header with account summary -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-semibold text-gray-800">Client Accounts</h1>
      <div class="flex space-x-2 relative">
        <button
          class="bg-blue-500 text-white text-sm px-4 py-2 rounded-md hover:bg-blue-600 shadow-sm"
          @click="showAddUserPopup = !showAddUserPopup"
        >
          + Add New User
        </button>
        <div
          class="profile-dropdown absolute top-10 left-5 bg-white shadow-md rounded-lg p-4"
          v-show="showAddUserPopup"
        >
          <div class="form-container">
            <label for="Owner" class="text-xs font-semibold mb-2"
              >User Number</label
            >
            <input
              type="number"
              placeholder="Owner ID"
              v-model="addUserId"
              class="w-[150px] border-[1.5px] border-gray-500 rounded-md mb-5 mt-2 text-sm px-4 py-2"
            />
            <div class="profile-dropdown-item">
              <button
                class="primary-button px-4 py-2 rounded-lg text-white bg-red-500 text-xs font-medium mx-auto block"
                @click="addUser"
              >
                Add User
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Parent Account Summary (Reduced font size and spacing) -->
    <div class="grid grid-cols-3 gap-4 mb-8">
      <div class="bg-white p-4 rounded-lg shadow-sm" v-if="parentAccount">
        <p class="text-xs text-gray-500">Total Balance</p>
        <h2 class="text-xl font-semibold text-gray-800">
          {{ formatCurrency(parentAccount.balance) }}
        </h2>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm">
        <p class="text-xs text-gray-500">Active Users</p>
        <h2 class="text-xl font-semibold text-gray-800">
          {{ activeChildAccountsLength }}
        </h2>
      </div>
      <div class="bg-white p-4 rounded-lg shadow-sm">
        <p class="text-xs text-gray-500">Inactive Users</p>
        <h2 class="text-xl font-semibold text-gray-800">
          {{ inactiveChildAccountsLength }}
        </h2>
      </div>
    </div>

    <!-- Active Child Accounts (with user avatars and compact spacing) -->
    <div>
      <h3 class="text-lg font-semibold text-gray-800 mb-3">Active Users</h3>
      <div class="grid grid-cols-3 gap-4">
        <div
          v-for="child in activeChildAccounts"
          :key="child.id"
          class="bg-white p-4 rounded-lg shadow-sm flex items-start space-x-4 relative"
        >
          <!-- Avatar Placeholder -->
          <div
            class="flex-shrink-0 w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center"
          >
            <vue-feather type="user" class="text-gray-500" />
          </div>

          <!-- User Info -->
          <div class="flex-1">
            <h4 class="text-sm font-semibold text-gray-900">
              {{ child.user.username }}
            </h4>
            <p class="text-xs text-gray-500">{{ child.user.email }}</p>
          </div>

          <!-- Dropdown Menu (More actions) -->
          <div class="absolute top-2 right-2">
            <button
              @click="toggleDropdown(child.id)"
              class="text-gray-500 hover:text-gray-800"
            >
              <vue-feather type="more-vertical" />
            </button>
            <div
              v-if="isDropdownOpen(child.id)"
              class="absolute right-0 mt-2 w-36 bg-white border border-gray-200 rounded-lg shadow-lg z-10"
            >
              <ul class="text-xs text-gray-700">
                <li class="p-2 hover:bg-gray-100 cursor-pointer">
                  Detail Account
                </li>
                <li
                  class="p-2 hover:bg-gray-100 cursor-pointer text-red-500"
                  @click="deactivateAccount(child)"
                >
                  Deactivate
                </li>
                <li class="p-2 hover:bg-gray-100 cursor-pointer text-red-500">
                  Remove
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Inactive Child Accounts (Similar compact design with avatars) -->
    <div class="mt-8">
      <h3 class="text-lg font-semibold text-gray-800 mb-3">Inactive Users</h3>
      <div class="grid grid-cols-3 gap-4">
        <div
          v-for="child in inactiveChildAccounts"
          :key="child.id"
          class="bg-white p-4 rounded-lg shadow-sm flex items-start space-x-4 relative"
        >
          <!-- Avatar Placeholder -->
          <div
            class="flex-shrink-0 w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center"
          >
            <vue-feather type="user" class="text-gray-500" />
          </div>

          <!-- User Info -->
          <div class="flex-1">
            <h4 class="text-sm font-semibold text-gray-900">
              {{ child.user.username }}
            </h4>
            <p class="text-xs text-gray-500">{{ child.user.email }}</p>

            <button
              class="mt-2 bg-blue-500 text-white text-xs px-3 py-1 rounded-md hover:bg-blue-600"
              @click="activateAccount(child)"
            >
              Activate
            </button>
          </div>

          <!-- Dropdown Menu (More actions) -->
          <div class="absolute top-2 right-2">
            <button
              @click="toggleDropdown(child.id)"
              class="text-gray-500 hover:text-gray-800"
            >
              <vue-feather type="more-vertical" />
            </button>
            <div
              v-if="isDropdownOpen(child.id)"
              class="absolute right-0 mt-2 w-36 bg-white border border-gray-200 rounded-lg shadow-lg z-10"
            >
              <ul class="text-xs text-gray-700">
                <li
                  class="p-2 hover:bg-gray-100 cursor-pointer"
                  @click="deactivateAccount(child)"
                >
                  Remove
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useToast } from "vue-toastification";

const parentAccount = ref(null);
const activeChildAccounts = ref([]);
const inactiveChildAccounts = ref([]);
const activeChildAccountsLength = ref(0);
const inactiveChildAccountsLength = ref(0);
var url = process.env.VUE_APP_BASE_URL;
var toast = useToast();
const dropdownOpen = ref(null);
const showAddUserPopup = ref(false);
const addUserId = ref(null);

const formatCurrency = (value) => {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value);
};
const toggleDropdown = (id) => {
  dropdownOpen.value = dropdownOpen.value === id ? null : id;
};
const isDropdownOpen = (id) => {
  return dropdownOpen.value === id;
};

const fetchParentAccount = async () => {
  try {
    var response = await axios.get(`${url}/payment/billing-profile/me`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    parentAccount.value = response.data;
  } catch (error) {
    if (error.response) {
      if (error.response.data) {
        toast.error(error.response.data.detail);
      }
    } else {
      toast.error("Could not deactivate user");
    }
    console.log(error);
  }
};

const fetchActiveChildAccounts = async () => {
  try {
    var response = await axios.get(
      `${url}/payment/client-account/active_users/`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    activeChildAccounts.value = response.data["results"];
    activeChildAccountsLength.value = response.data["count"];
  } catch (error) {
    console.log(error);
  }
};
const deactivateAccount = async (user) => {
  try {
    await axios.post(
      `${url}/payment/client-account/deactivate_user/`,
      {
        user_id: user.id,
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    fetchActiveChildAccounts();
    fetchInactiveChildAccounts();
  } catch (error) {
    if (error.response) {
      if (error.response.data) {
        toast.error(error.response.data.detail);
      }
    } else {
      toast.error("Could not deactivate user");
    }
    console.log(error);
  }
};
const activateAccount = async (user) => {
  try {
    await axios.post(
      `${url}/payment/client-account/activate_user/`,
      {
        user_id: user.id,
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    fetchInactiveChildAccounts();
    fetchActiveChildAccounts();
  } catch (error) {
    if (error.response) {
      if (error.response.data) {
        toast.error(error.response.data.detail);
      }
    } else {
      toast.error("Could not activate user");
    }
    console.log(error);
  }
};
const fetchInactiveChildAccounts = async () => {
  try {
    var response = await axios.get(
      `${url}/payment/client-account/inactive_users/`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    inactiveChildAccounts.value = response.data["results"];
    inactiveChildAccountsLength.value = response.data["count"];
  } catch (error) {
    console.log(error);
  }
};
const addUser = async () => {
  try {
    await axios.post(
      `${url}/payment/client-account/add_user/`,
      {
        user_id: addUserId.value,
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    fetchActiveChildAccounts();
    fetchInactiveChildAccounts();
  } catch (error) {
    if (error.response) {
      if (error.response.data) {
        toast.error(error.response.data.detail);
      }
    } else {
      toast.error("Could not add user");
    }
    console.log(error);
  }
};

onMounted(() => {
  fetchActiveChildAccounts();
  fetchInactiveChildAccounts();
  fetchParentAccount();
});
</script>
