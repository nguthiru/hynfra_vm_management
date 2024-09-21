<template>
  <div class="h-screen">Logging in with github...</div>
</template>
<script setup>

import { onMounted } from "vue";
import axios from "axios";
var url = process.env.VUE_APP_BASE_URL;

onMounted(() => {

  const code = new URLSearchParams(window.location.search).get("code");
  axios
    .post(`${url}/auth/github`, { code })
    .then((res) => {
      localStorage.setItem("token", res.data.access);
      window.location.href = "/";
    })
    .catch((err) => {
      console.log(err);
    });
});

</script>