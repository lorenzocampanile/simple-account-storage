<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue';

const NAVBAR_ENTRIES = ref([
  {'name': 'Accounts list', 'link': '/'},
  {'name': 'Add new account', 'link': '/add'},
]);

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
        <div class="nav-right">
          <div class="nav-item has-sub toggle-hover" id="dropdown">
            <a class="nav-dropdown-link">Menu</a>
            <ul class="dropdown-menu dropdown-animated" role="menu">
              <li v-for="entry in NAVBAR_ENTRIES" role="menu-item"><RouterLink :to="entry.link">{{ entry.name }}</RouterLink></li>
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
