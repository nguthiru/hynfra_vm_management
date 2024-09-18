<template>
  <div class="dashboard-page flex">
    <div class="dashboard-sidebar">
      <SideBar />
    </div>
    <div class="dashboard-content w-full">
      <DashHeader />
      <router-view />
    </div>
  </div>
</template>

<style lang="scss">
.profile-image {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}
.dashboard-content {
  background-color: #fafafa;
}
.dashboard-page {
  overflow: hidden;
}
</style>

<script setup>
import SideBar from "@/components/dashboard/SideBar.vue";
import DashHeader from "@/components/dashboard/DashHeader.vue";
</script>
