<script setup>
import { ref } from 'vue';
import { login } from '@/composables/login';
import { STATUS_CODES, sendHttpReq } from '@/composables/httpreq';
import router from '@/router';
import CryptoJS from 'crypto-js';

const username = ref('');
const password = ref('');
const passwordConfirm = ref('');
const signUpError = ref('');
const signUpFieldErrors = ref({});
const successMessage = ref('');

async function performSignUp(event) {
  let [ publicKey, encryptedPrivateKey ] = await generateKeysPair(password.value);

  let accountResponse = await sendHttpReq('POST', '/api/v1/auth/register/', {
    "email": username.value,
    "password": password.value,
    "password_confirm": passwordConfirm.value,
    "public_key": publicKey,
    "encrypted_private_key": encryptedPrivateKey,
  })

  function cleanForm() {
    username.value = '';
    password.value = '';
    passwordConfirm.value = '';
  }

  function cleanResponseMessages() {
    signUpError.value = '';
    signUpFieldErrors.value = {};
    successMessage.value = '';
  }

  let accountResponseData = {};
  switch (accountResponse.status) {
    case STATUS_CODES.OK_CREATED:
      cleanForm();
      cleanResponseMessages();
      accountResponseData = await accountResponse.json();
      successMessage.value = 'We sent a confirmation email. Please check your inbox 🥳.'
      break;
    case STATUS_CODES.PAYLOAD_ERROR:
      cleanResponseMessages();
      accountResponseData = await accountResponse.json();
      signUpFieldErrors.value = accountResponseData;
      signUpError.value = accountResponseData.non_field_errors.join(', ');
  }
}

// Generate the public/private key pair, which will be used for enrcypting
// and decrypting the passwords of this account.
//
// Returns both:
// - decoded version of the public key
// - decoded and encrypted (using passphrase) version of the private key
let generateKeysPair = async function(passphrase) {
  const { publicKey, privateKey } = await window.crypto.subtle.generateKey(
    {
      name: "RSA-OAEP",
      modulusLength: 2048,
      publicExponent: new Uint8Array([0x01, 0x00, 0x01]),
      hash: { name: "SHA-256" },
    },
    true,
    ["encrypt", "decrypt"]
  );

  let exportedPrivateKey = JSON.stringify(await window.crypto.subtle.exportKey("jwk", privateKey));
  let encryptedPrivateKey = CryptoJS.AES.encrypt(exportedPrivateKey, passphrase).toString();

  let exportedPublicKey = JSON.stringify(await window.crypto.subtle.exportKey("jwk", publicKey));

  return [ exportedPublicKey, encryptedPrivateKey ];
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
                    <div v-if="successMessage" class="col-12">
                      <div class="toast toast--success" style="width: auto;">
                        <p>{{ successMessage }}</p>
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
