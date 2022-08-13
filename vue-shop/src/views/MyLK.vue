<script>
import MyOrderPreview from '../components/MyOrderPreview.vue'
export default {
  components: {
    MyOrderPreview
  },
  /* Как конструктор, определяет переменные */ 
  data() {
      return {
          orders: [],
          login: '',
          password: '',
          key: localStorage.getItem('token')                        
      }
  },
  /* Выполнится один раз при загрузке страницы */
  async mounted() {
    if (this.key != false){
          let response2 = await fetch(`/api/order/all`, {headers: {key: this.key}})
          this.orders = await response2.json()
        }
  },
  methods: {
      async autorize(event) {
        event.preventDefault()

        let response = await fetch(`/api/sign_in`, {headers: {login: this.login, password: this.password}, method: "POST"})
        let response_json = await response.json()
        let key = response_json.key

        if (key != false){
          this.key = key
          let response2 = await fetch(`/api/order/all`, {headers: {key: key}})
          this.orders = await response2.json()
          localStorage.setItem('token', `${key}`)
        }
        else{
          alert("Не подходят, вводите еще раз")
        }
      },
      async sign_out(event) {
        event.preventDefault()
        let response = await fetch(`/api/sign_out`, {headers: {key: this.key}, method: 'POST'})
        this.key = null
        this.orders.length = 0
        localStorage.removeItem('token') 
      },
      async get_key(event) {
        return localStorage.getItem('token')   
      }  
    }
  }
</script>

<template>
  <div class="page">

      <div class="left">
          <form>
              <label for="login">Лоигин:</label><br>
              <input type="text" id="login" name="login" v-model = login><br>

              <label for="password">Пароль:</label><br>
              <input type="text" id="password" name="password" v-model = password><br>

              <button type="submit" class="btn" v-on:click="autorize" >Авторизоваться</button>
          </form>
      </div>

      <div class="left">
        <button class="btn" v-on:click="sign_out" >Выйти</button>
      </div>

      <div class="mainbody" v-for = "order in orders" :key ="order.id">
          <MyOrderPreview :order = order />   
      </div>

  </div>
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