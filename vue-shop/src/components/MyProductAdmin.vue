<script>
export default{
  props: {
    product: Object
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
      <button class="more">
        Редактировать
      </button>
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
