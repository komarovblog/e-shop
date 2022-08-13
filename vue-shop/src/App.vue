<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>


<template>

  <header>
    <div class="logo">
      <img src="@/assets/logo.svg"/>
    </div>
    <nav>
      <RouterLink to="/">Главная</RouterLink>
      <RouterLink to="/products">Каталог</RouterLink>
      <RouterLink to="/user">Личный кабиент</RouterLink>
    </nav>
  </header>
  
  <main>
    <HelloWorld msg="Python Junior " /> <!-- Комментарий -->
    <RouterView />   
  </main>

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
