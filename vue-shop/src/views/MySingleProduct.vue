<script>
export default {
    data() {
        return {
            product: {},
            user_name: "",
            user_phone: "",
            count: 1
        }
    },
    async mounted() {
        let prod_id = this.$route.params.productid
        let response = await fetch(`/api/products/${prod_id}`)
        let response_json = await response.json()
        this.product = response_json
        console.log(this.product)       
    },
    methods: {
        async make_order(event) {
            console.log("111")
            event.preventDefault()
            console.log("111")
            let data = {
              name: this.user_name,
              phone: this.user_phone,
              list_id_prod: [{id: this.product.id, count: this.count}]
            }
            const response = await fetch('/api/order', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
            })
        }
    }
}

</script>


<template>
  <div class="preview">
    <div class="img">
      <img src="@/assets/no_img.jpg" class="card-img" alt="...">
    </div>
    <div class="details">
      <h3 class="heading">
        {{product.name}}
      </h3>
    </div>
    <div class="params">
      <div class="naming">Характеристики</div>
      <div>Объем {{product.volume}} м3</div>
      <div>Цвет {{product.color}}</div>
    </div>
    <div class="price">
      <div class="naming">Цена</div>
      <div>{{product.price}}</div>
    </div>
  </div>

  <form>
    <label for="name">Ваше имя:</label><br>
    <input type="text" id="username" name="username" v-model = user_mame><br>

    <label for="min">Ваш телефон:</label><br>
    <input type="text" id="userphone" name="serphone" v-model = user_phone><br>

    <label for="min">Сколько:</label><br>
    <input type="text" id="count" name="count" v-model = count><br>


    <button type="submit" class="order" v-on:click="make_order" >
      Заказать
    </button>

  </form>
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