<template>
  <div class="content">
    <div class="container-fluid">
  <div>
    <card>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        id="input-group-1"
        label="Name:"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          v-model="form.name"
          required
          placeholder="eg: Production Logger"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Your Function Name:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.func_name"
          required
          placeholder="eg: helloworld"
          description="This must be [a-z] and can only be delimited by '-'"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-3" label="Your Function:" label-for="input-3">
        <b-form-input
          id="input-3"
          v-model="form.content"
          required
          placeholder="eg: def helloworld(): print('this is a message.')"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-4" label="Your Dependencies:" label-for="input-4">
        <b-form-input
          id="input-4"
          v-model="form.dependencies"
          required
          placeholder="eg: dataclasses"
          description="These would be the import statements at the top"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-5" label="Language:" label-for="input-5">
        <b-form-select
          id="input-4"
          v-model="form.language"
          :options="languages"
          required
        ></b-form-select>
      </b-form-group>

      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    <b-card class="mt-3" header="Form Data Result">
      <pre class="m-0">{{ form }}</pre>
    </b-card>
    </card>
  </div>
    </div></div>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        name: '',
        func_name: '',
        content: '',
        dependencies: '',
        language: 'Python',
      },
      languages: ['Python'],
      show: true,
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();

      axios.post('http://10.145.196.253:5000/create', this.form)
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    onReset(evt) {
      evt.preventDefault();
      // Reset our form values
      this.form.name = '';
      this.form.func_name = '';
      this.form.function = '';
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
};
</script>
<style>

</style>
