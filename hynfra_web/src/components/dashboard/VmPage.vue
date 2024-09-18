<template>
  <main id="vms-page">
    <div class="vms-page-header">
      <h1 class="text-xl font-semibold">Virtual Machines</h1>
      <div class="vms-page-header-actions">
        <RouterLink :to="{ name: 'vms-create' }">
          <button class="primary-button">
            <span class="text-sm">Create VM</span>
          </button>
        </RouterLink>
      </div>
    </div>

    <div class="vm-loading" v-if="fetching_items">
      <SpringSpinner />
    </div>
    <div class="vms-page-content" v-else>
      <VmItem v-for="vm_item in vm_items" :key="vm_item.id" :vm="vm_item" />
    </div>
  </main>
</template>
<script setup>
import VmItem from "@/components/dashboard/VmItem.vue";
import axios from "axios";
import { onMounted, ref } from "vue";
import { useToast } from "vue-toastification";
import { SpringSpinner } from "epic-spinners";
var vm_items = ref([]);
var fetching_items = ref(false);
var toast = useToast();
const get_vm_items = async () => {
  var url = process.env.VUE_APP_BASE_URL;
  try {
    fetching_items.value = true;
    var response = await axios.get(url + "/vms", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    });

    if (response.status == 200) {
      vm_items.value = response.data["results"];
    }
  } catch (error) {
    if (error.response) {
      console.log(error.response.data);
    }
    toast.error("An error has occured");
  } finally {
    fetching_items.value = false;
  }
};

onMounted(() => {
  //fetch Data from API
  get_vm_items();
});
</script>

<style lang="scss">
#vms-page {
  padding: 1rem;
}

.vms-page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.vms-page-header-actions {
  display: flex;
  gap: 1rem;
}

.vms-page-content {
  display: grid;
  height: 90vh;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  overflow: scroll;
}
</style>
