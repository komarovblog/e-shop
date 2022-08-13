<script>
import MyProductPreview from '../components/MyProductPreview.vue'
export default {
    components: {
        MyProductPreview
    },
    /* Определяем переменные*/ 
    data() {
        return {
            products: [],
            filter_name: '',
            filter_min: null,
            filter_max: null                      
        }
    },
    /* Выполнится один раз при загрузке страницы */
    async mounted() {
        let response = await fetch("/api/products")
        let response_json = await response.json()
        this.products = response_json.products
    },
    /* Описываем функции, которые будут выполняться при наступлении события */
    methods: {
        async filter_products(event) {
            event.preventDefault()

            let params = []
            if (this.filter_name != ''){
                params.push(`name=${this.filter_name}`)
            }
            if (this.filter_min != null){
                params.push(`price_min=${this.filter_min}`)
            }
            if (this.filter_max != null){
                params.push(`price_max=${this.filter_max}`)
            }
            let query = params.join('&')

            const response = await fetch(`/api/products?${query}`);
            let response_json = await response.json()
            this.products = response_json.products
        }
    }
}
</script>

<template>
    <div class="page">

        <div class="left">
            <form>
                <label for="name">Название</label><br>
                <input type="text" id="name" name="fname" v-model = filter_name><br>

                <label for="min">Цена, от:</label><br>
                <input type="text" id="min" name="min" v-model = filter_min><br>

                <label for="max">Цена, до:</label><br>
                <input type="text" id="max" name="max" v-model = filter_max><br>

                <button type="submit" class="btn" v-on:click="filter_products" >Отправить</button>
            </form>
        </div>

        <div class="mainbody" v-for = "product in products" :key ="product.id">
            <MyProductPreview :product = product />   
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
