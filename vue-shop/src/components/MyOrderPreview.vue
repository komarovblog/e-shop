<script>
export default{
  /* Это данные которые мы передаем при вызове компонента в файле, это как атрибуты класса */ 
  props: {
    order: Object
  },
  methods: {
    go_to_order(){
      this.$router.push({
        path: `/order/${this.product.id}`
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
      <h3 class="id">
        {{order.id}}
      </h3>
    </div>
    <div class="status">
      <div>Статус {{order.status}} м3</div>
    </div>
    <div class="phone">
      <div>Телефон {{order.phone}} м3</div>
    </div>
    <div class="user_id">
      <div>Юзер ID{{order.user_id}}</div>
    </div>

    <div class="prod" v-for = "prod in order.prod_in_order" :key ="prod.id">
      <h1>{{prod.name}}</h1>
    </div>

    Тут добавить вывод товаров

  </div>
</template>



<style scoped>
.preview {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  background-color: #f3f3f3;
  padding: 15px;
}
.card-img {
  width: 110px;
}



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
