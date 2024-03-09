<script setup>
import { RouterLink, RouterView } from 'vue-router'

// let dataCopyButtons = document.querySelectorAll('.data-copy-btn');
// for (let button of dataCopyButtons) {
//   button.addEventListener('click', () => {
//     let textToCopy = button.getAttribute('data-copy');
//     navigator.clipboard.writeText(textToCopy);
//     button.setAttribute('data-tooltip', 'Copied!');
//   })
// }
// console.log(dataCopyButtons);
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
              <li role="menu-item"><a href="/accounts/">Accounts list</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <section class="section">
      <RouterView />
    </section>
  </div>

</template>

<style scoped></style>
