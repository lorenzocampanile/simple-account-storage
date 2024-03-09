<script setup>
import { ref } from 'vue';
import { login } from '@/composables/login';

const username = ref('');
const password = ref('');

async function performLogin(event) {
  await login(username.value, password.value);
  console.log('*** res', sessionStorage.getItem('encryptionKey'));
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
              <div class="content">
                <div class="row u-gap-2 mt-3">
                  <div class="col-12">
                    <input v-model="username" type="text" placeholder="Username" />
                  </div>
                  <div class="col-12">
                    <input v-model="password" type="password" placeholder="Password" />
                  </div>
                </div>
              </div>
              <div class="card__action-bar u-center">
                <button class="btn-link" @click="performLogin">Sign in</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped>
  .card__image {
    background-image: url('/src/assets/images/login.jpg');
  }
</style>
