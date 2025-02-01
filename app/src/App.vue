<template>
  <Suspense>
    <template #default>
      <BetsScreen />
    </template>
    <template #fallback>
      <div class="flex items-center justify-center h-screen">
        <div class="spinner">Loading...</div>
      </div>
    </template>
  </Suspense>
</template>

<script setup>
import BetsScreen from "./components/BetsScreen.vue";
</script>
