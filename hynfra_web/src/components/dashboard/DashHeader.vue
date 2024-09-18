<template>
  <div
    class="dashboard-header w-full flex justify-end items-center gap-20 shadow-sm px-4 py-2"
  >
    <div class="dashboard-header-nav-links flex gap-8 justify-end">
      <RouterLink :to="{ name: 'payments' }">
        <div class="header-nav-link">
          <p class="text-xs font-medium">Subscription & Billing</p>
        </div>
      </RouterLink>
      <RouterLink :to="{ name: 'clients' }">
        <div class="header-nav-link">
          <p class="text-xs font-medium">Client Accounts</p>
        </div>
      </RouterLink>
    </div>
    <div class="dashboard-profile relative" v-if="profile">
      <div class="profile-info flex gap-2 items-center">
        <img
          class="profile-image"
          src="https://uxwing.com/wp-content/themes/uxwing/download/peoples-avatars/default-avatar-profile-picture-female-icon.png"
        />
        <p class="profile-name text-xs font-medium">{{ profile.username }}</p>
        <ChevronDownIcon @click="toggleLogoutBar" />
      </div>
      <div
        class="profile-dropdown absolute top-10 right-0 z-10 bg-white shadow-md rounded-lg p-4"
        v-show="openLogoutBar"
      >
        <div class="profile-dropdown-item">
          <p class="text-xs font-medium my-4">Profile ID: {{ profile.id }}</p>
        </div>
        <div class="profile-dropdown-item">
          <p class="text-xs font-medium my-4">Settings</p>
        </div>
        <div class="profile-dropdown-item">
          <button
            class="px-4 py-2 rounded-lg text-white bg-red-500 text-xs font-medium"
            my-4
            @click="logout"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ChevronDownIcon from "@/components/icons/ChevronDownIcon.vue";
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
const router = useRouter();
const profile = ref(null);
var url = process.env.VUE_APP_BASE_URL;
const openLogoutBar = ref(false);
const fetchProfile = async () => {
  try {
    const { data } = await axios.get(`${url}/auth/user/me/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    profile.value = data;
  } catch (error) {
    console.error(error);
  }
};

const toggleLogoutBar = () => {
  openLogoutBar.value = !openLogoutBar.value;
};

const logout = () => {
  localStorage.removeItem("token");
  router.replace({
    name: "login",
  });
};

onMounted(() => {
  fetchProfile();
});
</script>

<style scoped>
.dashboard-header {
  background-color: white;
  border-bottom: 1px solid rgba(128, 128, 128, 0.183);

  padding: 0.5rem 1rem;
}
.dashboard-profile {
  svg {
    width: 20px;
    height: 20px;
    cursor: pointer;
  }
}
.header-nav-link {
  cursor: pointer;
  p {
    font-weight: 500;
  }

  &:hover {
    text-decoration: underline;
  }
}
.router-link-active .header-nav-link {
  text-decoration: underline;
  color: #275bc3;
  p {
    font-weight: bold;
  }
}
</style>
