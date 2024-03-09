<script setup>
import { ref } from 'vue';
import { login } from '@/composables/login';
import { STATUS_CODES } from '@/composables/httpreq';
import router from '@/router';

const username = ref('');
const password = ref('');
const authenticationError = ref('');

async function performLogin(event) {
  let loginResponse = await login(username.value, password.value);

  if (loginResponse.status === STATUS_CODES.OK) {
    authenticationError.value = '';
    router.push({ path: '/' });
  }

  authenticationError.value = 'Invalid username or password.';
}
</script>

<template>
  <div class="hero fullscreen bg-gray-300">
    <div class="hero-body">
      <div class="content">
        <div class="row">
          <div class="col-12 u-center">
            <div class="card" style="max-width: 350px;">
              <div class="card__container">
                <div class="card__image">
                  <div class="bg-black u-opacity-70" style="width: 100%; height: 100%;"></div>
                </div>
                <div class="card__title-container">
                  <p class="title">Sign in</p><span class="subtitle">Insert username and password</span>
                </div>
              </div>
              <form @submit.prevent="performLogin">
                <div class="content">
                  <div class="row u-gap-2 mt-3">
                    <div v-if="authenticationError" class="col-12">
                      <div class="toast toast--danger" style="width: auto;">
                        <p>{{ authenticationError }}</p>
                      </div>
                    </div>
                    <div class="col-12">
                      <input v-model="username" type="text" placeholder="Username" />
                    </div>
                    <div class="col-12">
                      <input v-model="password" type="password" placeholder="Password" />
                    </div>
                  </div>
                </div>
                <div class="card__action-bar u-center">
                  <button type="submit">Sign in</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped>
.card__image {
  background-image: url('/images/login.jpg');
}
</style>
