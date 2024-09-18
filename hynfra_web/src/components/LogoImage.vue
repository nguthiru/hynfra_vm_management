<template>
  <img :src="logoSrc" alt="" class="w-36" />
</template>

<script>
export default {
  name: "LogoImage",
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    logoSrc() {
      return this.dark
        ? "https://hynfratech.com/wp-content/uploads/2022/11/Hynfra-Tech-HL-Logo-f.png"
        : "https://hynfratech.com/wp-content/uploads/2022/11/Hynfra-Tech-HL-Logo-f.png";
    },
  },
};
</script>
