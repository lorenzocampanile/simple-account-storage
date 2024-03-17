<script setup>
  import { ref, onMounted } from "vue";
  import { sendHttpReq } from '@/composables/httpreq';

  const loadingVerification = ref(true);
  const verificationError = ref(false);

  const QUERY_STRING = window.location.search;
  const URL_PARAMS = new URLSearchParams(QUERY_STRING);

  onMounted(async () => {
    let response = await sendHttpReq('POST', '/api/v1/accounts/verify-registration/', {
      "user_id": URL_PARAMS.get('user_id'),
      "timestamp": URL_PARAMS.get('timestamp'),
      "signature": URL_PARAMS.get('signature'),
    });
    let responseData = await response.json();
    if (response.status === 200) {
      loadingVerification.value = false;
    } else {
      verificationError.value = true
    }
  });
</script>

<template>
  <div class="bg-gray-100 u-center" style="height: 500px;">
    <p v-if="verificationError">We can't verify your e-mail, <RouterLink to="/signup">try again 😢</RouterLink></p>
    <p v-else-if="loadingVerification">We are verifing your e-mail...</p>
    <p v-else>E-Mail verified successfully 🥳🥳 <RouterLink to="/login">Go to login page</RouterLink></p>
  </div>
</template>