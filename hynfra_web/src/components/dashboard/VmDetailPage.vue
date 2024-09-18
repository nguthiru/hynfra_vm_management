<template>
  <div class="bg-[#fafafa] min-h-screen p-6 text-sm" v-if="vm_details">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="bg-white rounded-xl shadow-lg p-6 mb-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <div
              class="bg-gradient-to-br from-blue-400 to-indigo-500 w-16 h-16 rounded-xl flex items-center justify-center text-white text-2xl font-bold"
            >
              {{ vm_details["name"].charAt(0) }}
            </div>
            <div>
              <h1 class="text-2xl font-bold text-gray-800">
                {{ vm_details["name"] }}
              </h1>
              <p class="text-gray-500 text-sm">ID: {{ vm_details["id"] }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span
              :class="[
                'px-3 py-1 rounded-full text-xs font-medium',
                vm_details['status'] === 'running'
                  ? 'bg-green-100 text-green-800'
                  : vm_details['status'] === 'paused'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-red-100 text-red-800',
              ]"
            >
              {{
                vm_details["status"].charAt(0).toUpperCase() +
                vm_details["status"].slice(1)
              }}
            </span>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-3 gap-6">
        <!-- Left Column: VM Details and State Management -->
        <div class="col-span-2 space-y-6">
          <!-- VM Details -->
          <div class="bg-white rounded-xl shadow-lg p-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800">VM Details</h2>
            <div class="grid grid-cols-3 gap-4">
              <div class="bg-gray-50 p-4 rounded-lg text-center">
                <vue-feather
                  type="cpu"
                  class="w-8 h-8 mb-2 mx-auto text-gray-500"
                />
                <p class="text-xl font-bold text-gray-800">
                  {{ vm_details["cpu_core_count"] }}
                </p>
                <p class="text-xs text-gray-600">CPU Cores</p>
              </div>
              <div class="bg-gray-50 p-4 rounded-lg text-center">
                <vue-feather
                  type="server"
                  class="w-8 h-8 mb-2 mx-auto text-gray-500"
                />
                <p class="text-xl font-bold text-gray-800">
                  {{ vm_details["ram_size_gb"] }}GB
                </p>
                <p class="text-xs text-gray-600">RAM</p>
              </div>
              <div class="bg-gray-50 p-4 rounded-lg text-center">
                <vue-feather
                  type="hard-drive"
                  class="w-8 h-8 mb-2 mx-auto text-gray-500"
                />
                <p class="text-xl font-bold text-gray-800">
                  {{ vm_details["disk_size_gb"] }}GB
                </p>
                <p class="text-xs text-gray-600">Storage</p>
              </div>
            </div>
          </div>

          <!-- Instance State Management -->
          <div class="bg-white rounded-xl shadow-lg p-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800">
              Instance State
            </h2>
            <div
              class="flex justify-center space-x-3"
              v-if="vm_details['status'] !== 'deleted'"
            >
              <button
                @click="startVM"
                :class="[
                  'btn flex justify-center items-center flex-1 text-sm font-semibold',

                  vm_details['status'] === 'running' ? 'opacity-45' : '',
                ]"
              >
                <vue-feather type="play" class="w-4 h-4 mr-2" />
                Start
              </button>
              <button
                @click="stopVM"
                :class="[
                  'btn flex justify-center items-center flex-1 text-sm font-semibold',
                  vm_details['status'] === 'stopped' ? 'opacity-45' : '',
                ]"
              >
                <vue-feather type="pause" class="w-4 h-4 mr-2" />
                Stop
              </button>
              <button
                @click="confirmDeleteVM"
                class="btn btn-red flex justify-center items-center flex-1 text-sm text-red-600 font-semibold"
              >
                <vue-feather type="trash-2" class="w-4 h-4 mr-2" />
                Delete
              </button>
            </div>
            <div class="flex justify-center space-x-3" v-else>
              <p>VM has already been deleted</p>
            </div>
          </div>

          <!-- IP Address -->
          <div class="bg-white rounded-xl shadow-lg p-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800">Network</h2>
            <div
              class="flex items-center justify-between bg-gray-50 p-3 rounded-lg"
            >
              <div class="flex items-center space-x-3">
                <vue-feather type="globe" class="w-5 h-5 text-blue-500" />
                <span class="font-medium text-gray-700 text-sm"
                  >IP Address:</span
                >
              </div>
              <p class="text-gray-800 font-mono text-sm">
                <span v-if="vm_details['ip_address']">
                  {{ vm_details["ip_address"] }}
                </span>
                <span v-else>Not Available</span>
              </p>
            </div>
          </div>
        </div>

        <!-- Right Column: Transfer, Backup, and Backup History -->
        <div class="space-y-6">
          <!-- Transfer and Backup -->
          <div
            class="bg-white rounded-xl shadow-lg p-6"
            v-if="vm_details['status'] !== 'deleted'"
          >
            <h2 class="text-xl font-semibold mb-4 text-gray-800">VM Actions</h2>
            <div class="space-y-3">
              <button
                @click="showTransferModal = true"
                class="btn btn-indigo w-full justify-center text-sm"
              >
                <vue-feather type="send" class="w-4 h-4 mr-2" />
                Transfer VM
              </button>
              <button
                @click="showBackupModal = true"
                class="btn btn-purple w-full justify-center text-sm"
              >
                <vue-feather type="save" class="w-4 h-4 mr-2" />
                Create Backup
              </button>
            </div>
          </div>

          <!-- Backup History -->
          <div class="bg-white rounded-xl shadow-lg p-6">
            <h2 class="text-xl font-semibold mb-4 text-gray-800">
              Backup History
            </h2>
            <div class="space-y-3">
              <div
                v-for="backup in backups"
                :key="backup.id"
                class="bg-gray-50 p-3 rounded-lg"
              >
                <div class="flex justify-between items-center mb-1">
                  <span class="font-medium text-gray-700 text-sm">{{
                    formatDate(backup.created_at)
                  }}</span>
                  <span
                    :class="[
                      'px-2 py-1 rounded-full text-xs font-medium capitalize',
                      backup.status === 'created'
                        ? 'bg-green-100 text-green-800'
                        : backup.status === 'in-progress'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-red-100 text-red-800',
                    ]"
                  >
                    {{ backup.status }}
                  </span>
                </div>
                <p class="text-xs text-gray-600">
                  Size:
                  <span v-if="backup.backup_size">
                    {{ backup.backup_size }}GB
                  </span>
                  <span v-else>N/A</span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Transfer VM Modal -->
    <div
      v-if="showTransferModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-white p-6 rounded-xl w-80">
        <h2 class="text-xl font-semibold mb-4 text-gray-800">Transfer VM</h2>
        <div class="mb-4">
          <label
            for="userId"
            class="block text-sm font-medium text-gray-700 mb-1"
            >User ID</label
          >
          <input
            type="text"
            id="userId"
            v-model="transferUserId"
            class="w-full px-3 py-2 text-sm rounded-lg border-black focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
          />
        </div>
        <div class="flex justify-between space-x-3">
          <button
            @click="showTransferModal = false"
            class="btn btn-red-outline text-sm"
          >
            Cancel
          </button>
          <button
            @click="transferVM"
            class="btn btn-indigo text-sm text-red-500"
          >
            Transfer
          </button>
        </div>
      </div>
    </div>

    <!-- Create Backup Modal -->
    <div
      v-if="showBackupModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-white p-6 rounded-xl w-80">
        <h2 class="text-xl font-semibold mb-4 text-gray-800">Create Backup</h2>
        <div class="mb-4 space-y-1">
          <p class="text-sm text-gray-600">
            Estimated backup size:
            <span class="font-medium text-gray-800">{{
              vm_details["disk_size_gb"]
            }}</span>
          </p>
          <p class="text-sm text-gray-600">
            Estimated cost:
            <span class="font-medium text-gray-800"
              >${{ estimatedBackupCost }}</span
            >
          </p>
        </div>
        <div class="flex justify-between space-x-3">
          <button
            @click="showBackupModal = false"
            class="btn btn-red-outline text-sm"
          >
            Cancel
          </button>
          <button @click="createBackup" class="btn btn-purple text-sm">
            Create Backup
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-white p-6 rounded-xl w-80">
        <h2 class="text-xl font-semibold mb-4 text-gray-800">
          Confirm Deletion
        </h2>
        <p class="text-sm text-gray-600 mb-4">
          Are you sure you want to delete this VM? This action cannot be undone.
        </p>
        <div class="flex justify-between space-x-3">
          <button
            @click="showDeleteModal = false"
            class="btn btn-red-outline text-sm"
          >
            Cancel
          </button>
          <button @click="deleteVM" class="btn btn-red text-sm text-red-600">
            Delete VM
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="min-h-screen p-6 grid place-items-center" v-else>
    <spring-spinner color="black" />
  </div>
</template>
<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useToast } from "vue-toastification";
import { useRoute } from "vue-router";
import { SpringSpinner } from "epic-spinners";
const route = useRoute();
var url = process.env.VUE_APP_BASE_URL;

const loading = ref(false);
const backupLoading = ref(false);
var toast = useToast();
// VM data (replace with actual data fetching logic)
const vm_details = ref(null);

// Modals
const showTransferModal = ref(false);
const showBackupModal = ref(false);
const showDeleteModal = ref(false);

// Transfer VM
const transferUserId = ref("");
const transferVM = async () => {
  try {
    const response = await axios.post(
      `${url}/vms/${route.params.id}/transfer/`,
      {
        new_owner: transferUserId.value,
      },
      {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      }
    );
    if (response.status <= 210) {
      toast.success("VM transferred successfully");
    }
  } catch (error) {
    console.log(error);
    toast.error("Failed to transfer VM");
  } finally {
    showTransferModal.value = false;
  }
};

// Backup
const estimatedBackupCost = ref("....");

const getEstimatedBackupCost = async () => {
  try {
    const response = await axios.get(
      `${url}/vms/${route.params.id}/backup_cost/`,
      {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      }
    );
    if (response.status <= 210) {
      estimatedBackupCost.value = response.data["backup_cost"];
    }
  } catch (error) {
    console.log(error);
  }
};

const createBackup = async () => {
  try {
    const response = await axios.post(
      `${url}/vms/${route.params.id}/backup/`,
      {},
      {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      }
    );
    if (response.status <= 210) {
      toast.success("Backup created successfully");
      await get_backup_history();
    }
  } catch (error) {
    console.log(error);
    toast.error("Failed to create backup");
  } finally {
    showBackupModal.value = false;
  }
};
const startVM = async () => {
  if (vm_details.value["status"] == "running") {
    toast.error("VM is already running");
    return;
  }
  loading.value = true;
  try {
    const response = await axios.post(
      `${url}/vms/${route.params.id}/start/`,
      {},
      {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      }
    );
    if (response.status <= 210) {
      toast.success("VM started successfully");
      await get_vm_details();
    }
  } catch (error) {
    console.log(error);
    toast.error("Failed to start VM");
  } finally {
    loading.value = false;
  }
};

const stopVM = async () => {
  if (vm_details.value["status"] == "stopped") {
    toast.error("VM is already stopped");
  }
  loading.value = true;
  try {
    const response = await axios.post(
      `${url}/vms/${route.params.id}/stop/`,
      {},
      {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      }
    );
    if (response.status <= 210) {
      toast.success("VM stopped successfully");
      await get_vm_details();
    }
  } catch (error) {
    console.log(error);
    toast.error("Failed to stop VM");
  } finally {
    loading.value = false;
  }
};

const confirmDeleteVM = () => {
  showDeleteModal.value = true;
};

const formatDate = (value) => {
  const options = { year: "numeric", month: "long", day: "numeric" };
  return new Date(value).toLocaleDateString(undefined, options);
};

const deleteVM = async () => {
  // Implement delete VM logic
  console.log("Deleting VM");
  showDeleteModal.value = false;
  try {
    const response = await axios.delete(
      `${url}/vms/${route.params.id}/`,

      {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      }
    );
    if (response.status <= 210) {
      toast.success("VM deleted successfully");
      await get_vm_details();
    }
  } catch (error) {
    if (error.response) {
      toast.error("Failed to delete VM. Please try again or contact support.");
    }
  }
};

// Backup history (replace with actual data fetching logic)
const backups = ref([]);

const get_backup_history = async () => {
  try {
    backupLoading.value = true;
    var response = await axios.get(
      url + "/vms/" + route.params["id"] + "/backup_history/",
      {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      }
    );
    if (response.status == 200) {
      backups.value = response.data["results"];
    }
  } catch (error) {
    console.log(error);
  } finally {
    backupLoading.value = false;
  }
};

const get_vm_details = async () => {
  var url = process.env.VUE_APP_BASE_URL;
  try {
    loading.value = true;
    var response = await axios.get(url + "/vms/" + route.params["id"], {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    });

    if (response.status == 200) {
      vm_details.value = response.data;
    }
  } catch (error) {
    if (error.response) {
      console.log(error.response.data);
    }
    toast.error("An error has occured");
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  // TODO: Fetch VM data and backup history
  get_vm_details();
  get_backup_history();
  getEstimatedBackupCost();
});
</script>
<style scoped>
.btn {
  @apply flex items-center justify-center px-4 py-2 rounded-lg font-medium transition duration-150 ease-in-out text-white shadow-sm hover:shadow-md active:shadow-sm;
}

.btn-blue {
  @apply bg-blue-500 hover:bg-blue-600 active:bg-blue-700;
}

.btn-green {
  @apply bg-green-500 hover:bg-green-600 active:bg-green-700;
}

.btn-yellow {
  @apply bg-yellow-500 hover:bg-yellow-600 active:bg-yellow-700;
}

.btn-red {
  @apply bg-red-500 hover:bg-red-600 active:bg-red-700;
}

.btn-red-outline {
  @apply bg-white text-red-500 border border-red-500 hover:bg-red-50 active:bg-red-100;
}

.btn-indigo {
  @apply bg-indigo-500 hover:bg-indigo-600 active:bg-indigo-700;
}

.btn-purple {
  @apply bg-purple-500 hover:bg-purple-600 active:bg-purple-700;
}
</style>
