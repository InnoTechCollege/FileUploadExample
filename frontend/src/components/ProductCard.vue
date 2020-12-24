<template>
  <v-card max-width="300">
    <v-img max-height="150" :src="'/userImages/' + product[3]"> </v-img>
    <v-card-title class="magic-text">{{ product[1] }}</v-card-title>
    <v-card-subtitle>{{ product[2] }}</v-card-subtitle>
  </v-card>
</template>

<script>
export default {
  props: {
    product: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
</style>