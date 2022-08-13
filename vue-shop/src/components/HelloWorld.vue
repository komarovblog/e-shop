<script setup>
defineProps({
  msg: {
    type: String,
    required: true
  }
})
</script>

<template>

  <h1 class="my_h1">{{ msg }}</h1>
  <h3>Python, FastApi, SQL, Vue.js</h3>
  <div>Проект в портфолио для резюме Junior Python разрабочик. Простейший прототип интернет магазина, сервер написан на языке Python с использованием библиотеки FastApi.</div>

</template>

<style scoped>

@media (max-width: 767px) {
  /* стили для xs-устройств */
}
@media (min-width: 768px) and (max-width: 991px) {
  /* стили для sm-устройств */
}
@media (min-width: 991px) and (max-width: 1199px) {
  /* стили для md-устройств */
}
@media (min-width: 1200px) {
  /* стили для lg-устройств */
}
</style>
