<template>
  <div class="hello">
    <b-table striped hover :busy="isLoading" :items="functions">
      <template v-slot:table-busy>
        <div class="text-center text-danger my-2">
          <b-spinner class="align-middle"></b-spinner>
          <strong>Loading...</strong>
        </div>
      </template>
    </b-table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Table',
  data() {
    this.fetch_data();
    return {
      isLoading: true,
      functions: [
      ],
    };
  },
  methods: {
    fetch_data() {
      axios.get('http://localhost:3000/get_all')
        .then((response) => {
          this.functions = response.data;
          this.isLoading = false;
        });
    },
  },
};
</script>
