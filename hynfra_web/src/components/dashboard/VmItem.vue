<template>
  <router-link :to="{ name: 'vms-detail', params: { id: vm['id'] } }">
    <div class="vms-page-item">
      <div class="vm-page-content-item-header">
        <div class="flex gap-2">
          <img
            src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhUXYtZGaSVpgszvcdic5jZKt2rhQZqPGEng&s"
            class="w-10 h-10 rounded-md"
            alt=""
          />
          <div class="vm-item-header-details">
            <p class="font-semibold">{{ vm["name"] }}</p>
            <span class="text-sm text-gray-500">ID: VM_{{ vm["id"] }}</span>
          </div>
        </div>
      </div>
      <div class="divider h-[1px] w-auto bg-gray-200 my-4"></div>
      <div class="vm-item-status my-2">
        <p class="text-xs text-gray-500">Status</p>
        <div class="flex justify-between items-center">
          <p class="text-sm vm-status" :class="vm['status']">
            {{ vm["status"] }}
          </p>
          <div class="flex gap-4">
            <div class="icon-button pause">
              <vue-feather type="pause" />
            </div>
            <div class="icon-button trash">
              <vue-feather type="trash" />
            </div>
          </div>
        </div>
      </div>
      <div class="divider h-[1px] w-auto bg-gray-200 my-4"></div>

      <div class="vm-item-sizes flex flex-wrap justify-between">
        <div class="vm-item-sizes-item flex gap-1">
          <vue-feather type="cpu" />
          <p class="font-semibold">{{ vm["cpu_core_count"] }} Core</p>
        </div>
        <div class="vm-item-sizes-item flex gap-1">
          <vue-feather type="server" />
          <p class="font-semibold">{{ vm["ram_size_gb"] }} GB</p>
        </div>
        <div class="vm-item-sizes-item flex gap-1">
          <vue-feather type="hard-drive" />

          <p class="font-semibold">{{ vm["disk_size_gb"] }}GB</p>
        </div>
      </div>

      <div class="vm-item-ip flex gap-2 mt-6 items-center justify-center">
        <vue-feather type="terminal" />
        <p class="text-xs text-gray-500">
          <span v-if="vm['ip_address']">
            {{ vm["ip_address"] }}
          </span>
          <span v-else>
            <span class="text-gray-500">No IP address assigned</span>
          </span>
        </p>
      </div>
    </div>
  </router-link>
</template>

<style lang="scss">
.vms-page-item {
  background-color: white;
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease-out;
  &:hover {
    transform: scale(1.02);
  }
}

.vm-page-content-item-status ::after {
  content: "";
  display: block;
  width: 100%;
  height: 1px;
  background-color: rgba(128, 128, 128, 0.149);
  margin: 0.5rem 0;
}
.vm-status {
  text-transform: capitalize;
}
.vm-status.created {
  color: #bacc2e;
}
.vm-status.running {
  color: green;
}
.vm-status.paused {
  color: red;
}
.vm-status.stopped {
  color: gray;
}

.vm-status {
  font-weight: 500;
}
.vm-item-header-details {
  p {
    font-size: 0.9rem;
    font-weight: 600;
    height: 1rem;
  }

  span {
    font-size: 0.7rem;
    font-weight: 500;
  }
}

.vm-item-status {
  p {
    font-size: 0.8rem;
    font-weight: 500;
  }
}

.vms-page-item {
  .icon-button {
    display: grid;
    place-items: center;
    width: 30px;
    height: 30px;
    cursor: pointer;
    padding: 0.2rem;
    border-radius: 5px;
    background-color: #afc7f97b;
    transition: all 0.3s ease-out;

    svg {
      width: 20px;
      height: 20px;
    }
  }

  .icon-button.trash {
    background-color: #f7d7d7;

    &:hover {
      background-color: #f97474;
    }
  }
  .icon-button.pause {
    background-color: #e0d7f7;

    &:hover {
      background-color: #b7a7f7;
    }
  }
}
.vm-item-sizes {
  svg {
    width: 20px;
    height: 20px;
  }
  font-size: 0.8rem;
  color: rgb(140, 140, 140);
}
.vm-item-ip {
  width: 100%;
  padding: 0.25rem 0.5rem;
  background-color: rgba(128, 128, 128, 0.088);
  border-radius: 10px;
  svg {
    width: 15px;
    height: 15px;
    path {
      fill: rgb(140, 140, 140);
    }
  }
  font-size: 0.8rem;
}
</style>
<script setup>
import { defineProps } from "vue";
const props = defineProps({
  vm: {
    type: Object,
    required: true,
  },
});

console.log(props);
</script>
