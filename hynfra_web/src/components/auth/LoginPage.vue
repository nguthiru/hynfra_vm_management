<template>
  <div>
    <div class="container">
      <h1 class="login-header">Welcome Back</h1>
      <p class="text-center text-sm font-semibold text-gray-500 mt-1">
        Welcome Back. Please Sign In
      </p>
    </div>
    <form @submit.prevent="login">
      <div class="form-container">
        <label for="">Username</label>

        <input
          type="name"
          v-model="username"
          placeholder="xxx@xxx.com"
          class="w-full my-2"
        />
      </div>
      <div class="form-container">
        <label for="">Password</label>
        <input
          type="password"
          v-model="password"
          placeholder="Password"
          class="w-full my-2"
        />
      </div>
      <span
        class="forgot-password-text my-[10px] ml-auto text-sm font-semibold underline"
        >Forgot Password?</span
      >
      <button type="button" class="primary-button w-full my-1" @click="login">
        <spring-spinner v-if="loading" size="22" class="mx-auto" />
        <span class="ml-2" v-else>Login</span>
      </button>
      <span
        class="text-center my-[10px] block cursor-pointer text-sm font-semibold underline"
        @click="guestLogin"
        >Login As Guest</span
      >
      <div
        class="text-overlay-divider h-[1px] w-full relative bg-gray-400 my-4"
      >
        <span
          class="absolute top-[-10px] left-1/2 transform -translate-x-1/2 bg-white px-1"
        >
          OR
        </span>
      </div>
      <button type="button" class="w-full outline-button my-2">
        <div class="flex justify-center">
          <img
            src="https://img.icons8.com/color/48/000000/google-logo.png"
            alt=""
            class="w-6 h-6"
          />
          <span class="ml-2">Sign in with Google</span>
        </div>
      </button>
    </form>
    <p class="text-center font-semibold text-sm mt-4">
      Don't Have an Account?
      <router-link
        :to="{ name: 'register' }"
        class="font-bold text-sm underline"
        >Sign Up</router-link
      >
    </p>
  </div>
</template>
<style lang="scss">
.login-header {
  font-size: 1.7rem;
  font-weight: bold;
  text-align: center;
}

.form-container {
  margin: 1em 0;

  label {
    font-size: small;
    font-weight: gray;
    font-weight: 500;
  }
}
input {
  height: 50px;
  padding: 0 20px;
  border-radius: 10px;
  border: 1.2px solid grey;

  &::placeholder {
    font-size: small;
  }
}

.primary-button,
.outline-button {
  min-height: 45px;
}
.forgot-password-text {
  margin-left: auto;
  text-align: end;
  display: block;
  margin: 10px 0;
}
</style>

<script setup>
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";

import { SpringSpinner } from "epic-spinners";
var username = ref("");
var password = ref("");
var loading = ref(false);
var router = useRouter();
var toast = useToast();
var login = async () => {
  loading.value = true;
  try {
    var url = process.env.VUE_APP_BASE_URL;
    var response = await axios.post(url + "/auth/token/", {
      username: username.value,
      password: password.value,
    });
    if (response.status === 200) {
      localStorage.setItem("token", response.data.access);
      toast.success("Login Successful");
      return router.replace({ name: "dashboard" });
    }
  } catch (error) {
    if (error.response) {
      toast.error("Check Your Username or Password");
    } else {
      toast.error("Network error");
    }
  } finally {
    loading.value = false;
  }
};
var guestLogin = async () => {
  try {
    var url = process.env.VUE_APP_BASE_URL;
    var response = await axios.post(url + "/auth/guest-login/");
    if (response.status === 200) {
      localStorage.setItem("token", response.data.access);
      toast.success("Guest Login Successful");
      return router.replace({ name: "dashboard" });
    }
  } catch {
    toast.error("Guest Login Not Available");
  }
};
</script>
