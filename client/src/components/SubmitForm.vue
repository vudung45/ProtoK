<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset">
      <b-form-group
        id="input-group-1"
        label="Name:"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          v-model="form.name"
          required
          trim
          placeholder="eg: production-logger"
        ></b-form-input>
        <b-form-invalid-feedback>
          Please use all lower-case and delimited by a - or .
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group id="input-group-2" label="Your Function Name:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.func_name"
          required
          trim
          placeholder="eg: helloworld"
          description="This must be [a-z] and can only be delimited by '-'"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-3" label="Your Function:" label-for="input-3">
        <b-form-input
          id="input-3"
          v-model="form.content"
          required
          trim
          placeholder="eg: def helloworld(): print('this is a message.')"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-4" label="Your Dependencies:" label-for="input-4">
        <b-form-input
          id="input-4"
          v-model="form.dependencies"
          trim
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

      <b-button
        :disabled="shouldDisableButtons"
        class="mr-2"
        type="submit"
        variant="primary"
      >
       Submit
      </b-button>
      <b-button type="reset" :disabled="shouldDisableButtons" variant="danger">Reset</b-button>
    </b-form>

    <b-alert
      :show="shouldShowAlert"
      :variant=variant
      class="mt-3"
    >
      {{alertMessage}}
    </b-alert>

    <b-spinner class="mt-3" v-if="shouldDisableButtons" label="Loading..."></b-spinner>

    <b-card class="mt-3" header="Form Data Result" v-if="debug">
      <pre class="m-0">{{ form }}</pre>
    </b-card>
  </div>
</template>

<script>
import axios from 'axios';
import { debugEnabled } from '@/variables';

export default {
  name: 'HelloWorld',
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
      variant: 'primary',
      shouldShowAlert: false,
      alertMessage: '',
      debug: debugEnabled,
      shouldDisableButtons: false,
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.shouldDisableButtons = true;

      axios.post('http://localhost:5000/create', this.form)
        .then((response) => {
          console.log(response);
          this.variant = 'success';
          this.alertMessage = 'Successfully ran the function.';
          this.shouldShowAlert = true;
          this.shouldDisableButtons = false;
        })
        .catch((error) => {
          console.log(error);
          this.variant = 'danger';
          this.alertMessage = 'Something went wrong...';
          this.shouldShowAlert = true;
          this.shouldDisableButtons = false;
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
