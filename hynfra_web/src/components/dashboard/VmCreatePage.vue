<template>
  <main id="vm-create-page" class="p-6">
    <div class="vm-create-page-header">
      <h1 class="text-xl font-semibold">Create Virtual Machine</h1>
    </div>
    <div
      class="vm-create-form p-6 bg-white rounded-lg shadow max-w-[768px] mx-auto my-4"
    >
      <form action="" class="form" @submit.prevent="createVm">
        <div class="form-group">
          <div class="flex justify-between">
            <div class="form-details">
              <p class="form-details-name">Machine Name</p>
              <p class="form-details-desc">
                A unique name for the virtual machine
              </p>
            </div>
            <div class="form-container w-1/2">
              <input type="text" id="vm-name" class="input" v-model="vmName" />
            </div>
          </div>
        </div>
        <div class="form-group">
          <div class="flex justify-between">
            <div class="form-details">
              <p class="form-details-name">Operating System</p>
              <p class="form-details-desc">VM Operating System</p>
            </div>
            <div class="form-container w-1/2">
              <input type="text" id="vm-name" class="input" v-model="vmOs" />
            </div>
          </div>
        </div>
        <div class="form-group">
          <div class="justify-between">
            <div class="form-details">
              <p class="form-details-name">Machine Size</p>
              <p class="form-details-desc">CPU Cores, Memory Size, Disk Size</p>
            </div>
            <div class="flex justify-between my-4">
              <div class="form-container">
                <label for="vm-name" class="label">CPU Cores</label>
                <input type="text" id="vm-name" class="input" v-model="vmCpu" />
              </div>
              <div class="form-container">
                <label for="vm-name" class="label">RAM Size</label>
                <input type="text" id="vm-name" class="input" v-model="vmRam" />
              </div>
              <div class="form-container">
                <label for="vm-name" class="label">Disk Size</label>
                <input
                  type="text"
                  id="vm-name"
                  class="input"
                  v-model="vmDisk"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="form-group">
          <div class="flex justify-between">
            <div class="form-details">
              <p class="form-details-name">Machine Owner</p>
              <p class="form-details-desc">VM Owner</p>
            </div>
            <div class="form-container w-1/2">
              <label for="vm-name" class="label">Owner</label>
              <input
                type="number"
                id="vm-owner"
                class="input"
                v-model="vmOwner"
              />
            </div>
          </div>
        </div>
        <button class="primary-button ml-auto block" @click="createVm">
          <spring-spinner v-if="loading" size="22" class="mx-auto" />
          <span class="ml-2" v-else>Create VM</span>
        </button>
      </form>
    </div>
  </main>
</template>
<script setup>
import { ref } from "vue";
import { SpringSpinner } from "epic-spinners";
import axios from "axios";
import { useToast } from "vue-toastification";
import { useRouter } from "vue-router";

var toast = useToast();
var router = useRouter();
const vmName = ref("");
const vmOs = ref("");
const vmCpu = ref("");
const vmRam = ref("");
const vmDisk = ref("");
const vmOwner = ref("");
var fieldErrors = ref({});
const loading = ref(false);
var url = process.env.VUE_APP_BASE_URL;
const createVm = async () => {
  loading.value = true;
  var data = {
    name: vmName.value,
    os: vmOs.value,
    cpu_core_count: vmCpu.value,
    ram_size_gb: vmRam.value,
    disk_size_gb: vmDisk.value,
    owner: vmOwner.value,
  };
  try {
    var response = await axios.post(`${url}/vms/`, data, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    if (response.status === 201) {
      toast.success("VM Created Successfully");
      router.push({ name: "dashboard" });
    }
  } catch (error) {
    if (error.response) {
      if (error.response.data.detail) {
        toast.error(error.response.data.detail);
      } else {
        fieldErrors.value = error.response.data;
        toast.error("Error Creating VM");
      }
    } else {
      toast.error("Error Creating VM");
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style lang="scss" scoped>
.form-container {
  label {
    display: block;
    font-size: smaller;
    font-weight: 500;
  }

  input {
    width: 100%;
    padding: 0.3rem 0.5rem;
    margin-top: 0.5rem;
    border: 1px solid #9ea0a2;
    border-radius: 0.25rem;
    height: 35px;
    font-size: small;
    font-weight: 500;
  }
}

.form-group {
  margin: 1rem 0;

  &::after {
    content: "";
    display: block;
    width: 100%;
    height: 1px;
    background-color: #e5e7eb;
    margin: 1rem 0;
  }
}

.form-details {
  font-size: small;

  .form-details-name {
    font-weight: 600;
  }

  .form-details-desc {
    margin: 0.5rem 0;
    font-size: 0.75rem;
  }
}
</style>
