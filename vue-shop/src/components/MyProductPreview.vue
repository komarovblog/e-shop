<script>
export default{
  /* Это данные которые мы передаем при вызове компонента в файле, это как атрибуты класса */ 
  props: {
    product: Object
  },
  methods: {
    go_to_product(){
      this.$router.push({
        path: `/products/${this.product.id}`
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
    <div id = {{product.id}}>
      <button class="more" v-on:click="go_to_product">
        Подробнее
      </button>
    </div>
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
