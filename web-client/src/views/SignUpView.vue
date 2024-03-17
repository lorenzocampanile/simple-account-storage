<script setup>
import { ref } from 'vue';
import { login } from '@/composables/login';
import { STATUS_CODES, sendHttpReq } from '@/composables/httpreq';
import router from '@/router';

const username = ref('');
const password = ref('');
const passwordConfirm = ref('');
const signUpError = ref('');
const signUpFieldErrors = ref({});

async function performSignUp(event) {
  let accountResponse = await sendHttpReq('POST', '/api/v1/auth/register/', {
    "email": username.value,
    "password": password.value,
    "password_confirm": passwordConfirm.value,
  })

  let accountResponseData = {};
  switch (accountResponse.status) {
    case STATUS_CODES.OK_CREATED:
      signUpError.value = '';
      signUpFieldErrors.value = {};
      accountResponseData = await accountResponse.json();
      console.log('*** ', accountResponseData);
      break;
    case STATUS_CODES.PAYLOAD_ERROR:
      signUpError.value = '';
      signUpFieldErrors.value = {};
      accountResponseData = await accountResponse.json();
      console.log('*** ', accountResponseData);
      signUpFieldErrors.value = accountResponseData;
      signUpError.value = accountResponseData.non_field_errors.join(', ');
  }
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
                  <p class="title">Sign up</p><span class="subtitle">Create an account</span>
                </div>
              </div>
              <form @submit.prevent="performSignUp">
                <div class="content">
                  <div class="row u-gap-2 mt-3">
                    <div v-if="signUpError" class="col-12">
                      <div class="toast toast--danger" style="width: auto;">
                        <p>{{ signUpError }}</p>
                      </div>
                    </div>
                    <div class="col-12">
                      <input v-model="username" type="email" placeholder="E-Mail" />
                      <span class="info ml-1 text-danger" v-if="signUpFieldErrors.email">{{ signUpFieldErrors.email.join(',') }}</span>
                    </div>
                    <div class="col-12">
                      <input v-model="password" type="password" placeholder="Password" />
                      <span class="info ml-1 text-danger" v-if="signUpFieldErrors.password">{{ signUpFieldErrors.password.join(',') }}</span>
                    </div>
                    <div class="col-12">
                      <input v-model="passwordConfirm" type="password" placeholder="Password confirmation" />
                      <span class="info ml-1 text-danger" v-if="signUpFieldErrors.password_confirm">{{ signUpFieldErrors.password_confirm.join(',') }}</span>
                    </div>
                  </div>
                </div>
                <div class="card__action-bar u-center">
                  <button type="submit">Sign up</button>
                </div>
                <div class="card__footer">
                  <div class="u-text-center"><span>Do you already have an account? <RouterLink to="/login">Sign in!</RouterLink></span></div>
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
