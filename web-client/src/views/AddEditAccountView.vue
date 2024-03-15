<script setup>
import { STATUS_CODES, sendHttpReq } from '@/composables/httpreq';
import router from '@/router';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const ACCOUNT_TYPES = {
  WEB_PORTAL: 'web',
  SSH_SERVER: 'ssh',
  DATABASE: 'database',
}

const successMessage = ref('');
const fieldErrorMessages = ref({});

const accountLabel = ref('');
const accountUsername = ref('');
const showPassword = ref(false);
const accountPassword = ref('');
const accountNotes = ref('');
const accountType = ref('');
const accountWebLink = ref('');
const accountSshLink = ref('');
const accountDatabaseHost = ref('');
const accountDatabaseType = ref('');

// If requested, show the success message
const QUERY_STRING = window.location.search;
const URL_PARAMS = new URLSearchParams(QUERY_STRING);
const showSuccessCreatedMessage = ref(URL_PARAMS.get('showSuccessCreatedMessage') === 'true');
const showSuccessEditedMessage = ref(URL_PARAMS.get('showSuccessEditedMessage') === 'true');

// If I'm editing a page, fetch the current object data
let route = useRoute();
let accountId = route.params.id ?? null;
onMounted(async () => {
  if (route.params.id) {
    let accountResponse = await sendHttpReq('GET', `/accounts/api/${accountId}`);

    let accountData = await accountResponse.json();
    accountLabel.value = accountData.label;
    accountUsername.value = accountData.label;
    accountPassword.value = accountData.password;
    accountNotes.value = accountData.notes;
    accountType.value = accountData.type;
    accountWebLink.value = accountData.web ? accountData.web.link : null;
    accountSshLink.value = accountData.ssh ? accountData.ssh.link : null;
    accountDatabaseHost.value = accountData.database ? accountData.database.host : null;
    accountDatabaseType.value = accountData.database ? accountData.database.type : null;
  }
});


async function saveAccount(event) {
  // Define the base payload
  let accountPayload = {
    label: accountLabel.value,
    username: accountUsername.value,
    password: accountPassword.value,
    notes: accountNotes.value,
    type: accountType.value,
  };

  // Add specific data about the account type
  switch (accountType.value) {
    case ACCOUNT_TYPES.WEB_PORTAL:
      accountPayload['web'] = {'link': accountWebLink.value};
      break;
    case ACCOUNT_TYPES.SSH_SERVER:
      accountPayload['ssh'] = {'link': accountSshLink.value};
      break;
    case ACCOUNT_TYPES.DATABASE:
      accountPayload['database'] = {'host': accountDatabaseHost.value, 'type': accountDatabaseType.value};
      break;
  }

  // Send the HTTP request and handle the response
  let httpMethod = accountId ? 'PATCH' : 'POST';
  let url = accountId ? `/accounts/api/${accountId}/` : '/accounts/api/';
  let accountResponse = await sendHttpReq(httpMethod, url, accountPayload);
  let accountResponseJson = await accountResponse.json();
  switch (accountResponse.status) {
    case STATUS_CODES.OK_CREATED:
      fieldErrorMessages.value = {};
      router.push(`/edit/${accountResponseJson.id}?showSuccessCreatedMessage=true`);
      break;
    case STATUS_CODES.OK:
      fieldErrorMessages.value = {};
      router.push(`/edit/${accountResponseJson.id}?showSuccessEditedMessage=true`);
      showSuccessCreatedMessage.value = false;
      showSuccessEditedMessage.value = true;
      break;
    case STATUS_CODES.PAYLOAD_ERROR:
      successMessage.value = '';
      fieldErrorMessages.value = accountResponseJson;
      break;
  }
}
</script>

<template>
  <div class="hero fullscreen bg-gray-300">
    <div class="hero-body">
      <div class="content">
        <div class="row">
          <div class="col-12 u-center">
            <div class="card" style="max-width: 550px;">
              <div class="card__container">
                <div class="card__image">
                  <div class="bg-black u-opacity-70" style="width: 100%; height: 100%;"></div>
                </div>
                <div v-if="accountId" class="card__title-container">
                  <p class="title">Edit account credentials</p><span class="subtitle">Edit the credentials of this account.</span>
                </div>
                <div v-else class="card__title-container">
                  <p class="title">Add account credentials</p><span class="subtitle">Save the credentials of a new account.</span>
                </div>
              </div>
              <form @submit.prevent="saveAccount">
                <div class="content">
                  <div class="row u-gap-2 mt-3">
                    <div v-if="fieldErrorMessages.non_field_errors" class="col-12">
                      <div class="toast toast--danger" style="width: auto;">
                        <p>{{ fieldErrorMessages.non_field_errors.join(',') }}</p>
                      </div>
                    </div>
                    <div v-if="successMessage" class="col-12">
                      <div class="toast toast--success" style="width: auto;">
                        <p>{{ successMessage }}</p>
                      </div>
                    </div>
                    <div v-if="showSuccessCreatedMessage" class="col-12">
                      <div class="toast toast--success" style="width: auto;">
                        <p>Account created successfully.</p>
                      </div>
                    </div>
                    <div v-if="showSuccessEditedMessage" class="col-12">
                      <div class="toast toast--success" style="width: auto;">
                        <p>Account edited successfully.</p>
                      </div>
                    </div>
                    <div class="col-12">
                      <input v-model="accountLabel" type="text" placeholder="Label for the account" />
                      <span class="info ml-1 text-danger" v-if="fieldErrorMessages.label">{{ fieldErrorMessages.label.join(',') }}</span>
                    </div>
                    <div class="col-12">
                      <input v-model="accountUsername" type="text" placeholder="Username" />
                      <span class="info ml-1 text-danger" v-if="fieldErrorMessages.username">{{ fieldErrorMessages.username.join(',') }}</span>
                    </div>
                    <div class="col-12 row">
                      <div class="col-10 p-0">
                        <input v-if="showPassword" v-model="accountPassword" type="text" placeholder="Password" />
                        <input v-else v-model="accountPassword" type="password" placeholder="Password" />
                        <span class="info ml-1 text-danger" v-if="fieldErrorMessages.password">{{ fieldErrorMessages.password.join(',') }}</span>
                      </div>
                      <div class="col-1 ml-1"><button @click.prevent="showPassword = !showPassword">Show</button></div>
                    </div>
                    <div class="col-12">
                      <textarea v-model="accountNotes" placeholder="Notes" />
                      <span class="info ml-1 text-danger" v-if="fieldErrorMessages.notes">{{ fieldErrorMessages.notes.join(',') }}</span>
                    </div>
                    <div class="col-12">
                      <select v-model="accountType">
                        <option value="">Select account type</option>
                        <option value="web">Web portal</option>
                        <option value="ssh">SSH server</option>
                        <option value="database">Database</option>
                      </select>
                      <span class="info ml-1 text-danger" v-if="fieldErrorMessages.type">{{ fieldErrorMessages.type.join(',') }}</span>
                    </div>
                    <div class="col-12" v-if="accountType === 'web'">
                      <input v-model="accountWebLink" type="text" placeholder="Web link (e.g. www.facebook.com/login)" />
                      <span class="info ml-1 text-danger" v-if="fieldErrorMessages.web && fieldErrorMessages.web.link">{{ fieldErrorMessages.web.link.join(',') }}</span>
                    </div>
                    <div class="col-12" v-if="accountType === 'ssh'">
                      <input v-model="accountSshLink" type="text" placeholder="SSH Link (e.g. user@88.88.88.88)" />
                      <span class="info ml-1 text-danger" v-if="fieldErrorMessages.ssh && fieldErrorMessages.ssh.link">{{ fieldErrorMessages.ssh.link.join(',') }}</span>
                    </div>
                    <div class="col-12" v-if="accountType === 'database'">
                      <input v-model="accountDatabaseHost" type="text" placeholder="Database host (e.g. 88.88.88.88)" />
                      <span class="info ml-1 text-danger" v-if="fieldErrorMessages.database && fieldErrorMessages.database.host">{{ fieldErrorMessages.database.host.join(',') }}</span>
                      <select v-model="accountDatabaseType" class="mt-1">
                        <option value="">Select database type</option>
                        <option value="mysql">MySQL</option>
                        <option value="mariadb">MariaDB</option>
                        <option value="postgresql">PostgreSQL</option>
                        <option value="oracle">Oracle Database</option>
                        <option value="other">Other</option>
                      </select>
                      <span class="info ml-1 text-danger" v-if="fieldErrorMessages.database && fieldErrorMessages.database.type">{{ fieldErrorMessages.database.type.join(',') }}</span>
                    </div>
                  </div>
                </div>
                <div class="card__action-bar u-center">
                  <input type="submit" value="Save account" />
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
