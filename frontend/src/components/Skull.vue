<template>
  <div>
    <p>API URL: {{ apiUrl }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      apiUrl: process.env.VUE_APP_ROOT_API,
    };
  },
  created() {
    console.log("VUE_APP_ROOT_API:", process.env.VUE_APP_ROOT_API);
  },
};
</script>
