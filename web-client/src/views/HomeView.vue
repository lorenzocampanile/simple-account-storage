<script setup>
import { sendHttpReq } from '@/composables/httpreq';
import router from '@/router';
import { onMounted, ref } from 'vue';

const QUERY_STRING = window.location.search;
const URL_PARAMS = new URLSearchParams(QUERY_STRING);
let currentPage = URL_PARAMS.get(parseInt(URL_PARAMS.get('page'))) ?? 1;

let accounts = ref([]);

// Fetch the user's Account(s)
onMounted(async () => {
  let accountsResponse = await sendHttpReq('GET', `/accounts/api`, {'page': currentPage});
  let accountsResponseData = await accountsResponse.json();
  accounts.value = accountsResponseData['results'];
});

let getIconStlyeFromAccount = (account) => {
  const ACCOUNT_TYPE_ICON_MAP = {
    web: 'fa-globe',
    ssh: 'fa-server',
    database: 'fa-database',
  };

  return ACCOUNT_TYPE_ICON_MAP[account.type ?? 'web'];
}

let goToEditAccountPage = (account) => {
  router.push(`/edit/${account.id}`);
}

let copiedRefs = ref({
  usernames: [],
  loadingPasswords: [],
  passwords: [],
  webLinks: [],
  sshLinks: [],
  databaseHosts: [],
});

let getCopyButtonTooltipText = (account, type) => {
  if (type === 'passwords' && copiedRefs.value['loadingPasswords'].indexOf(account.id) >= 0) {
    return 'Loading...';
  }

  if (copiedRefs.value[type].indexOf(account.id) >= 0) {
    return 'Copied to clipboard!';
  }

  return 'Click to copy';
}

let copyAccountPropertyToClipboard = (account, propName) => {
  const PROP_NAME_COPIED_LIST_MAP = {
    'username': 'usernames',
    'web.link': 'webLinks',
    'ssh.link': 'sshLinks',
    'db.host': 'databaseHosts',
  };

  if (propName.indexOf('.') >= 0) {
    let propNameParts = propName.split('.');
    navigator.clipboard.writeText(account[propNameParts[0]][propNameParts[1]]);
  } else {
    navigator.clipboard.writeText(account[propName]);
  }

  copiedRefs.value[PROP_NAME_COPIED_LIST_MAP[propName]].push(account.id);
  setTimeout(() => {
    copiedRefs.value[PROP_NAME_COPIED_LIST_MAP[propName]].pop(account.id);
  }, 1000);
}

let copyPasswordToClipboard = async (account) => {
  let url = `/accounts/api/${account.id}`;
  copiedRefs.value.loadingPasswords.push(account.id);
  let accountResponse = await sendHttpReq('GET', url);
  let accountResponseData = await accountResponse.json();
  copiedRefs.value.loadingPasswords.pop(account.id);

  navigator.clipboard.writeText(accountResponseData['password']);
  copiedRefs.value.passwords.push(account.id);
  setTimeout(() => {
    copiedRefs.value.passwords.pop(account.id);
  }, 1000);
}

</script>

<template>
  <div class="hero fullscreen bg-gray-300">
    <div class="hero-body">
      <div class="content">

        <div class="p-4">
          <h3>Accounts list</h3>
          <div v-for="account in accounts" class="card">
            <div class="card__header">
              <p class="font-bold px-3">
                <i class="fa fa-solid" :class="getIconStlyeFromAccount(account)"></i> -
                {{ account.label }}
              </p>
              <p>{{ account.notes }}</p>
            </div>
            <div class="card__action-bar u-right">
              <button class="data-copy-btn btn bg-gray-600 text-white" @click="goToEditAccountPage(account)">Edit account</button>
              <button class="data-copy-btn btn bg-green-400 text-white tooltip" :data-tooltip="getCopyButtonTooltipText(account, 'usernames')" @click="copyAccountPropertyToClipboard(account, 'username')">Copy username</button>
              <button class="data-copy-btn btn bg-gray-600 text-white tooltip" :data-tooltip="getCopyButtonTooltipText(account, 'passwords')" @click="copyPasswordToClipboard(account)">Copy password</button>
              <button v-if="account.type === 'web'" class="data-copy-btn btn btn-link tooltip" :data-tooltip="getCopyButtonTooltipText(account, 'webLinks')" @click="copyAccountPropertyToClipboard(account, 'web.link')">Copy web link</button>
              <button v-if="account.type === 'ssh'" class="data-copy-btn btn bg-indigo-600 text-white tooltip" :data-tooltip="getCopyButtonTooltipText(account, 'sshLinks')" @click="copyAccountPropertyToClipboard(account, 'ssh.link')">Copy SSH link</button>
              <button v-if="account.type === 'database'" class="data-copy-btn btn bg-teal-600 text-white tooltip" :data-tooltip="getCopyButtonTooltipText(account, 'databaseHosts')" @click="copyAccountPropertyToClipboard(account, 'db.host')">Copy database host</button>
              <small class="text-gray-500">Created at: {{ account.created_at }}</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
