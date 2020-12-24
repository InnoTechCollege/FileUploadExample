<template>
  <div>
    <v-container>
      <v-row justify="center">
        <h1 class="magic-text">Magical Burgers</h1>
      </v-row>
    </v-container>

    <product-form @contentPosted="appendProducts"></product-form>
    <div id="product-container">
      <product-card
        v-for="product in products"
        :key="product[0]"
        :product="product"
      ></product-card>
    </div>
  </div>
</template>

<script>
import ProductCard from "@/components/ProductCard.vue";
import ProductForm from "@/components/ProductForm.vue";
import axios from "axios";

export default {
  components: {
    ProductCard,
    ProductForm,
  },
  data() {
    return {
      products: [],
    };
  },
  mounted() {
    this.getProducts();
  },
  methods: {
    getProducts() {
      axios
        .request({
          method: "GET",
          url: "http://localhost:5000/api/products",
        })
        .then((response) => {
          console.log(response);
          this.products = response.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    appendProducts(product) {
      this.products.push(product);
    },
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Lobster+Two:ital,wght@1,700&display=swap");

.magic-text {
  font-family: "Lobster Two", cursive;
  font-weight: bold;
  background: #ca4246;
  background-color: #ca4246;
  background-image: linear-gradient(
    45deg,
    #ca4246 16.666%,
    #e16541 16.666%,
    #e16541 33.333%,
    #f18f43 33.333%,
    #f18f43 50%,
    #8b9862 50%,
    #8b9862 66.666%,
    #476098 66.666%,
    #476098 83.333%,
    #a7489b 83.333%
  );
  background-size: 50%;
  background-repeat: repeat;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

#product-container {
  display: grid;
  justify-items: center;
  align-items: center;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  row-gap: 30px;
  column-gap: 30px;
  padding: 20px 5px;
}
</style>