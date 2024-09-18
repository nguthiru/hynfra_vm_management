<template>
  <div class="primary-body h-screen">
    <div class="page-center-container py-20">
      <div class="login-image m-auto w-40">
        <LogoImage class="" />
      </div>
      <div class="w-[400px] mx-auto my-10">
        <RouterView />
      </div>
    </div>
  </div>
</template>
<script setup>
import LogoImage from "@/components/LogoImage.vue";
</script>

<style lang="scss">
.page-center-container {
  display: grid;
  place-items: center;
}
.login-image {
  img {
    width: 100%;
    height: 100%;
    border-radius: 20px;
  }
}
</style>
