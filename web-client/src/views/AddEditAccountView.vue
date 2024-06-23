<script setup>
import { STATUS_CODES, sendHttpReq } from '@/composables/httpreq';
import router from '@/router';
import { onMounted, ref } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { encryptPassword, decryptPassword } from '@/composables/encryptor';


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
const accountSshHost = ref('');
const accountDatabaseHost = ref('');
const accountDatabaseType = ref('');

const showDeleteConfirmModal = ref(false);

// If requested, show the success message
const QUERY_STRING = window.location.search;
const URL_PARAMS = new URLSearchParams(QUERY_STRING);
const showSuccessCreatedMessage = ref(URL_PARAMS.get('showSuccessCreatedMessage') === 'true');
const showSuccessEditedMessage = ref(URL_PARAMS.get('showSuccessEditedMessage') === 'true');
const showSuccessDeleteMessage = ref(URL_PARAMS.get('showSuccessDeleteMessage') === 'true')

// If I'm editing a page, fetch the current object data
let route = useRoute();
let accountId = route.params.id ?? null;
onMounted(async () => {
  if (route.params.id) {
    let accountResponse = await sendHttpReq('GET', `/api/v1/accounts/${accountId}/`);

    let accountData = await accountResponse.json();
    accountLabel.value = accountData.label;
    accountUsername.value = accountData.label;
    accountNotes.value = accountData.notes;
    accountType.value = accountData.type;
    accountWebLink.value = accountData.web ? accountData.web.link : null;
    accountSshHost.value = accountData.ssh ? accountData.ssh.host : null;
    accountDatabaseHost.value = accountData.database ? accountData.database.host : null;
    accountDatabaseType.value = accountData.database ? accountData.database.type : null;

    // Decrypt the password
    let decryptedPassword = await decryptPassword(accountData.password);
    accountPassword.value = decryptedPassword;
  }
});

async function saveAccount(event) {
  // Encrypt the password
  let b64EncryptedPassword = await encryptPassword(accountPassword.value);

  // Define the base payload
  let accountPayload = {
    label: accountLabel.value,
    username: accountUsername.value,
    password: b64EncryptedPassword,
    notes: accountNotes.value,
    type: accountType.value,
  };

  // Add specific data about the account type
  switch (accountType.value) {
    case ACCOUNT_TYPES.WEB_PORTAL:
      accountPayload['web'] = {'link': accountWebLink.value};
      break;
    case ACCOUNT_TYPES.SSH_SERVER:
      accountPayload['ssh'] = {'host': accountSshHost.value};
      break;
    case ACCOUNT_TYPES.DATABASE:
      accountPayload['database'] = {'host': accountDatabaseHost.value, 'type': accountDatabaseType.value};
      break;
  }

  // Send the HTTP request and handle the response
  let httpMethod = accountId ? 'PATCH' : 'POST';
  let url = accountId ? `/api/v1/accounts/${accountId}/` : '/api/v1/accounts/';
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

async function deleteAccount() {
  let url = `/api/v1/accounts/${accountId}/`;
  let accountResponse = await sendHttpReq('DELETE', url);
  switch (accountResponse.status) {
    case STATUS_CODES.NO_CONTENT:
      fieldErrorMessages.value = {};
      router.push(`/add?showSuccessDeleteMessage=true`);
      break;
    case STATUS_CODES.PAYLOAD_ERROR:
      successMessage.value = '';
      break;
  }
}
</script>

<template>
  <div>
    <!-- Delete account modal -->
    <div class="modal" :class="{'modal--visible': showDeleteConfirmModal}" id="example-modal"><a onclick="toggleModal" class="modal-overlay close-btn" aria-label="Close"></a>
      <div class="modal-content" role="document">
        <div class="modal-header u-flex u-justify-space-between">
          <div class="modal-title">Delete account "{{ accountLabel }}"</div>
          <div @click="showDeleteConfirmModal = false" aria-label="Close"><span class="icon" style="cursor: pointer;"><svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="times" class="u-inline-block fa-times w-2 h-4 fa-wrapper" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 352 512"><path fill="currentColor" d="M242.72 256l100.07-100.07c12.28-12.28 12.28-32.19 0-44.48l-22.24-22.24c-12.28-12.28-32.19-12.28-44.48 0L176 189.28 75.93 89.21c-12.28-12.28-32.19-12.28-44.48 0L9.21 111.45c-12.28 12.28-12.28 32.19 0 44.48L109.28 256 9.21 356.07c-12.28 12.28-12.28 32.19 0 44.48l22.24 22.24c12.28 12.28 32.2 12.28 44.48 0L176 322.72l100.07 100.07c12.28 12.28 32.2 12.28 44.48 0l22.24-22.24c12.28-12.28 12.28-32.19 0-44.48L242.72 256z"></path></svg></span></div>
        </div>
        <div class="modal-body">
            Are you sure you want to delete this account?
        </div>
        <div class="modal-footer u-text-right">
          <button class="btn--sm" @click="showDeleteConfirmModal = false">Cancel</button>
          <button class="btn-primary btn--sm ml-2" @click="deleteAccount">Confirm delete</button>
        </div>
      </div>
    </div>

    <!-- Account form card -->
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
                <form>
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
                          <p>Account created successfully. <RouterLink to="/"><u>Go to the accounts list page.</u></RouterLink></p>
                        </div>
                      </div>
                      <div v-if="showSuccessEditedMessage" class="col-12">
                        <div class="toast toast--success" style="width: auto;">
                          <p>Account edited successfully. <RouterLink to="/"><u>Go to the accounts list page.</u></RouterLink></p>
                        </div>
                      </div>
                      <div v-if="showSuccessDeleteMessage" class="col-12">
                        <div class="toast toast--success" style="width: auto;">
                          <p>Account deleted successfully. <RouterLink to="/"><u>Go to the accounts list page.</u></RouterLink></p>
                        </div>
                      </div>
                      <div class="col-12">
                        <input v-model="accountLabel" type="text" placeholder="Label for the account" />
                        <span class="info ml-1 text-danger" v-if="fieldErrorMessages.label">{{ fieldErrorMessages.label.join(',') }}</span>
                      </div>
                      <div class="col-12">
                        <input v-model="accountUsername" type="text" placeholder="Username" autocomplete="off" readonly onfocus="this.removeAttribute('readonly');" />
                        <span class="info ml-1 text-danger" v-if="fieldErrorMessages.username">{{ fieldErrorMessages.username.join(',') }}</span>
                      </div>
                      <div class="col-12 row">
                        <div class="col-10 p-0">
                          <input v-if="showPassword" v-model="accountPassword" type="text" placeholder="Password" autocomplete="off" readonly onfocus="this.removeAttribute('readonly');" />
                          <input v-else v-model="accountPassword" type="password" placeholder="Password" autocomplete="off" readonly onfocus="this.removeAttribute('readonly');" />
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
                        <input v-model="accountWebLink" type="text" placeholder="Web link (e.g. https://www.facebook.com/login)" />
                        <span class="info ml-1 text-danger" v-if="fieldErrorMessages.web && fieldErrorMessages.web.link">{{ fieldErrorMessages.web.link.join(',') }}</span>
                      </div>
                      <div class="col-12" v-if="accountType === 'ssh'">
                        <input v-model="accountSshHost" type="text" placeholder="SSH Server Host (e.g. 88.88.88.88)" />
                        <span class="info ml-1 text-danger" v-if="fieldErrorMessages.ssh && fieldErrorMessages.ssh.host">{{ fieldErrorMessages.ssh.host.join(',') }}</span>
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
                    <button class="btn btn-success" @click.prevent="saveAccount">Save account</button>
                    <button v-if="accountId !== null" class="btn btn-danger" @click.prevent="showDeleteConfirmModal = true">Delete account</button>
                  </div>
                </form>
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
  background-image: url('/images/login.jpg');
}
</style>
