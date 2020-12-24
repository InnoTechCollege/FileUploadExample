<template>
  <div>
    <v-container>
      <v-row justify="center">
        <v-col xs="11" sm="10" md="6" lg="3">
          <v-card id="product-form-card">
            <v-form ref="form" id="product-form">
              <v-text-field
                name="name"
                label="Product Name"
                required
              ></v-text-field>
              <v-text-field
                name="description"
                label="Product Description"
                required
              ></v-text-field>
              <v-file-input
                name="image"
                id="image-upload-input"
                label="Product Image"
                accept="image/png, image/jpg, image/jpeg"
                required
                show-size
                :rules="imageRules"
              ></v-file-input>
              <v-btn @click="uploadProduct()">Submit</v-btn>
            </v-form>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <v-snackbar v-model="snackbar" :timeout="2000">
      {{ uploadStatus }}
      <template v-slot:action="{ attrs }">
        <v-btn color="blue" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      snackbar: false,
      uploadStatus: "",
      imageRules: [
        (value) =>
          !value ||
          value.size < 1000000 ||
          "Product image size must be < 1 MB!",
      ],
    };
  },
  methods: {
    uploadProduct() {
      let formEntries = document.getElementById("product-form");
      let formData = new FormData(formEntries);

      axios
        .request({
          url: "http://localhost:5000/api/products",
          method: "POST",
          headers: { "Content-Type": "multipart/form-data" },
          data: formData,
        })
        .then((response) => {
          console.log(response);
          this.$emit("contentPosted", response.data);
          this.$refs.form.reset();
          this.snackbar = true;
          this.uploadStatus = "Product Uploaded!";
        })
        .catch((err) => {
          console.log(err);
          this.snackbar = true;
          this.uploadStatus = "Upload Failed, Sorry!";
        });
    },
  },
};
</script>

<style scoped>
#product-form-card {
  padding: 30px 10px;
}
</style>