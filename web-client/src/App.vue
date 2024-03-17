<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { onMounted, ref } from 'vue';
import { logout, isUserAuthenticated } from '../src/composables/login';
import router from './router';

const NAVBAR_ENTRIES = ref([
  {'name': 'Accounts list', 'link': '/'},
  {'name': 'Add new account', 'link': '/add'},
]);

let performLogout = async () => {
  await logout();
}

</script>

<template>
  <div>
    <div class="header header-fixed unselectable header-animated">
      <div class="header-brand">
        <div class="nav-item no-hover">
          <h6 class="title">Simple Account Storage</h6>
        </div>
        <div class="nav-item nav-btn" id="header-btn"> <span></span> <span></span> <span></span> </div>
      </div>
      <div class="header-nav" id="header-menu">
        <div class="nav-left">

        </div>
        <div v-if="isUserAuthenticated()" class="nav-right">
          <div class="nav-item has-sub toggle-hover" id="dropdown">
            <a class="nav-dropdown-link">Menu</a>
            <ul class="dropdown-menu dropdown-animated" role="menu">
              <li v-for="entry in NAVBAR_ENTRIES" role="menu-item"><RouterLink :to="entry.link">{{ entry.name }}</RouterLink></li>
              <li role="menu-item"><a href="#" @click.prevent="performLogout">Logout</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <section class="section">
      <RouterView :key="$route.fullPath" />
    </section>
  </div>

</template>

<style scoped></style>
