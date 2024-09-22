<template>
  <div>
    <div class="container">
      <h1 class="login-header">Create an Account</h1>
      <p class="text-center text-sm font-semibold text-gray-500 mt-1">
        Join us to create Hynfra
      </p>
    </div>
    <form @submit.prevent="login">
      <p class="error text-sm font-semibold bg-red-600 mb-2" v-if="error">
        {{ error }}
      </p>
      <div class="form-container">
        <label for="">Username</label>

        <input
          type="text"
          v-model="username"
          placeholder=""
          class="w-full my-1"
        />
      </div>
      <div class="form-container">
        <label for="">Email Address</label>

        <input
          type="email"
          v-model="email"
          placeholder="xxx@xxx.com"
          class="w-full my-1"
        />
      </div>
      <div class="form-container">
        <label for="">Password</label>
        <input
          type="password"
          v-model="password"
          placeholder="Password"
          class="w-full my-1"
        />
      </div>
      <div class="form-container">
        <label for="">Confirm Password</label>
        <input
          type="password"
          v-model="password2"
          placeholder="Password"
          class="w-full my-1"
        />
      </div>
      <span
        class="forgot-password-text my-[10px] ml-auto text-sm font-semibold underline"
        >Forgot Password?</span
      >
      <button
        type="button"
        class="primary-button w-full my-1"
        @click="register"
      >
        <spring-spinner v-if="loading" size="22" class="mx-auto" />
        <span class="ml-2" v-else>Sign Up</span>
      </button>
      <div
        class="text-overlay-divider h-[1px] w-full relative bg-gray-400 my-4"
      >
        <span
          class="absolute top-[-10px] left-1/2 transform -translate-x-1/2 bg-white px-1"
        >
          OR
        </span>
      </div>
      <button
        type="button"
        class="w-full outline-button my-2"
        @click="githubLogin"
      >
        <div class="flex justify-center">
          <img
            src="https://w7.pngwing.com/pngs/646/324/png-transparent-github-computer-icons-github-logo-monochrome-head-thumbnail.png"
            alt=""
            class="w-6 h-6"
          />
          <span class="ml-2">Sign in with Github</span>
        </div>
      </button>
    </form>
    <p class="text-center font-semibold text-sm mt-4">
      Have an Account?
      <router-link :to="{ name: 'login' }" class="font-bold text-sm underline"
        >Login</router-link
      >
    </p>
  </div>
</template>
<style lang="scss" scoped>
.login-header {
  font-size: 1.7rem;
  font-weight: bold;
  text-align: center;
}

.form-container {
  margin: 0.5em 0;

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
var email = ref("");
var password = ref("");
var username = ref("");
var password2 = ref("");
var router = useRouter();
var loading = ref(false);
var toast = useToast();
var error = ref("");
const register = async () => {
  if (
    email.value === "" ||
    password.value === "" ||
    username.value === "" ||
    password2.value === ""
  ) {
    error.value = "Please fill all fields";
  } else if (password.value !== password2.value) {
    error.value = "Passwords do not match";
  } else {
    loading.value = true;
    try {
      var url = process.env.VUE_APP_BASE_URL;
      var response = await axios.post(url + "/auth/register/", {
        username: username.value,
        email: email.value,
        password: password.value,
        password2: password2.value,
      });
      if (response.status === 201) {
        toast.success("Sign Up Successful. Login");
        router.push({ name: "login" });
      }
    } catch (error) {
      if (error.response) {
        error.value = error.response.data;
      }
      console.log(error);
    } finally {
      loading.value = false;
    }
  }
};
var githubLogin = async () => {
  const clientId = "Ov23li6or8KFW37866Ve";
  const redirectUri = "http://localhost:8080/auth/sso-login/?sso=github"; // Your redirect URI
  const scope = "user";
  const githubAuthUrl = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}`;

  window.location.href = githubAuthUrl;
};
</script>
