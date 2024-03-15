<script setup>
import { defineProps } from 'vue';

defineProps(['pageCount', 'currentPage', 'previousPageLink', 'nextPageLink', 'styleClasses']);
</script>

<template>
  <div class="pagination pagination-bordered" :class="styleClasses">
    <div v-if="previousPageLink" class="bg-white pagination-item short"><RouterLink :to="'/?page=' + (currentPage - 1)">Prev</RouterLink></div>
    <div v-for="i in pageCount" class="pagination-item short" :class="currentPage === i ? 'selected' : 'bg-white'"><RouterLink :to="'/?page=' + i">{{ i }}</RouterLink></div>
    <div v-if="nextPageLink" class="bg-white pagination-item short"><RouterLink :to="'/?page=' + (currentPage + 1)">Next</RouterLink></div>
  </div>
</template>