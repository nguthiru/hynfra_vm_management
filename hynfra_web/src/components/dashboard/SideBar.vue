<template>
  <div
    id="dashboard-sidebar"
    class="h-screen py-6 px-6 min-w-[220px] shadow-md"
  >
    <LogoImage />
    <div class="nav-links-group my-4">
      <p class="nav-links-group-title">Instances</p>
      <RouterLink :to="{ name: 'vms' }">
        <div class="nav-link flex gap-2">
          <VirtualMachineIcon />
          <p>Virtual Machines</p>
        </div>
      </RouterLink>
      <div class="nav-link flex gap-2">
        <BackupIcon />
        <p>Backups</p>
      </div>
    </div>
    <div class="nav-links-group my-4">
      <p class="nav-links-group-title">Web & Email</p>
      <div class="nav-link flex gap-2">
        <WebIcon />
        <p>Web Hosting</p>
      </div>
      <div class="nav-link flex gap-2">
        <vue-feather type="mail" />
        <p>Email Hosting</p>
      </div>
    </div>
    <div class="nav-links-group my-4">
      <p class="nav-links-group-title">Voice</p>
      <div class="nav-link flex gap-2">
        <vue-feather type="headphones" />
        <p>VoIP</p>
      </div>
    </div>
  </div>
</template>
<script setup>
import LogoImage from "@/components/LogoImage.vue";
import VirtualMachineIcon from "@/components/icons/VirtualMachineIcon.vue";
import BackupIcon from "@/components/icons/BackupIcon.vue";
import WebIcon from "@/components/icons/WebIcon.vue";
</script>
<style lang="scss">
#dashboard-sidebar {
  border-right: 1px solid rgba(128, 128, 128, 0.474);
  // overflow-y: scroll;
}

.nav-links-group {
  margin-bottom: 2rem;
}

.nav-links-group-title {
  font-size: small;
  color: gray;

  &::after {
    content: "";
    display: block;
    width: 100%;
    height: 1px;
    background-color: rgba(128, 128, 128, 0.149);
    margin: 0.5rem 0;
  }
}

.nav-link {
  padding: 0.5rem 0.75rem;
  margin: 1rem 0;
  border-radius: 7px;
  cursor: pointer;
  transition: background-color 0.3s;
  transition: scale 0.3s ease-out;
  font-size: 0.85rem;
  font-weight: 500;

  &:hover {
    background-color: rgba(128, 128, 128, 0.1);
  }

  svg {
    width: 20px;
    height: 20px;
    // fill: white;
  }
}

.router-link-active .nav-link {
  padding: 0.5rem 0.8rem;

  background-color: #275bc3;
  color: white;

  svg,
  path {
    fill: white;
  }

  scale: 1.01;
}
</style>
