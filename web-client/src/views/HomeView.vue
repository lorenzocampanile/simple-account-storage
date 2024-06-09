<script setup>
import { sendHttpReq } from '@/composables/httpreq';
import router from '@/router';
import { onMounted, ref, watch, reactive } from 'vue';
import HomePaginator from '@/components/HomePaginator.vue';
import debounce from 'lodash.debounce'

const QUERY_STRING = window.location.search;
const URL_PARAMS = new URLSearchParams(QUERY_STRING);
const DEBOUNCE_MS = 300;

let currentPage = parseInt(URL_PARAMS.get('page') ?? 1);

let accounts = ref([]);
let previousPageLink = ref(null);
let nextPageLink = ref(null);
let pageCount = ref(1);

let formFilters = reactive({
  type: '',
  textSearch: '',
});


onMounted(async () => {
  await fetchAccountsData();
});

watch(formFilters, async (_, __) => {
  debounce(async () => {
    await fetchAccountsData();
  }, DEBOUNCE_MS)();
})


// Fetch the user's Account(s)
let fetchAccountsData = async function() {
  let params = {'page': currentPage};
  if (formFilters.type) params['type'] = formFilters.type
  if (formFilters.textSearch) params['search'] = formFilters.textSearch

  let accountsResponse = await sendHttpReq('GET', `/api/v1/accounts/`, params);
  let accountsResponseData = await accountsResponse.json();
  accounts.value = enrichAccountsResponseData(accountsResponseData['results']);

  previousPageLink.value = accountsResponseData['previous'];
  nextPageLink.value = accountsResponseData['next'];

  pageCount.value = parseInt(accountsResponseData['count'] / 10) + 1;
  if (accountsResponseData['count'] % 10 === 0) {
    pageCount.value = accountsResponseData['count'] / 10;
  }
}

// Enrich the accounts response data by adding some additional fields
let enrichAccountsResponseData = function(accountsResponseData) {
  for (let account of accountsResponseData) {
    // Add SSH link
    if ('ssh' in account) {
      account['ssh']['link'] = `ssh ${account['username']}@${account['ssh']['host']}`;
    }
  }

  return accountsResponseData;
}

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
  sshHosts: [],
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
    'ssh.host': 'sshHosts',
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
  let url = `/api/v1/accounts/${account.id}/`;
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
  <div class="fullscreen bg-gray-300">
    <div class="mt-4">
      <div class="content">
        <div class="p-4">
          <h3>Accounts list</h3>
          <div class="card">
            <div class="row">
              <div class="col-3">
                <select v-model="formFilters.type" class="select">
                  <option value="">All accounts types</option>
                  <option value="web">Web</option>
                  <option value="ssh">SSH</option>
                  <option value="database">Database</option>
                </select>
              </div>
              <div class="col-3">
                <input v-model="formFilters.textSearch" type="text" placeholder="Search by text" />
              </div>
            </div>
          </div>
          <div class="divider mt-4"></div>
          <div v-if="accounts.length > 0">
            <HomePaginator :pageCount="pageCount" :currentPage="currentPage" :previousPageLink="previousPageLink" :nextPageLink="nextPageLink" styleClasses="mb-2" />
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
                <button v-if="account.type === 'ssh'" class="data-copy-btn btn bg-teal-600 text-white tooltip" :data-tooltip="getCopyButtonTooltipText(account, 'sshHosts')" @click="copyAccountPropertyToClipboard(account, 'ssh.host')">Copy SSH host</button>
                <button v-if="account.type === 'ssh'" class="data-copy-btn btn bg-indigo-600 text-white tooltip" :data-tooltip="getCopyButtonTooltipText(account, 'sshLinks')" @click="copyAccountPropertyToClipboard(account, 'ssh.link')">Copy SSH link</button>
                <button v-if="account.type === 'database'" class="data-copy-btn btn bg-teal-600 text-white tooltip" :data-tooltip="getCopyButtonTooltipText(account, 'databaseHosts')" @click="copyAccountPropertyToClipboard(account, 'db.host')">Copy database host</button>
                <small class="text-gray-500">Created at: {{ account.created_at }}</small>
              </div>
            </div>
            <HomePaginator :pageCount="pageCount" :currentPage="currentPage" :previousPageLink="previousPageLink" :nextPageLink="nextPageLink" styleClasses="mt-2" />
          </div>
          <div v-else>
            <p>You don't have any saved account yes, <RouterLink to="/add">create one 😎</RouterLink></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
