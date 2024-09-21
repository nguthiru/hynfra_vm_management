<template>
  <div class="h-screen">
    <div class="flex flex-col gap-3 justify-center items-center"></div>
    Logging in with github...

    <SpringSpinner size="100" color="blue" />
  </div>
</template>
<script setup>
import { onMounted } from "vue";
import { SpringSpinner } from "epic-spinners";
import axios from "axios";
var url = process.env.VUE_APP_BASE_URL;

onMounted(() => {
  const code = new URLSearchParams(window.location.search).get("code");
  axios
    .post(`${url}/auth/github-login/`, { code: code })
    .then((res) => {
      localStorage.setItem("token", res.data.access);
      window.location.href = "/";
    })
    .catch((err) => {
      console.log(err);
    });
});
</script>
