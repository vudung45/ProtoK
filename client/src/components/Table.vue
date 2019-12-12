<template>
  <div class="hello">
    <b-alert
      :show="shouldShowAlert"
      :variant=variant
      class="mt-3"
    >
      {{alertMessage}}
    </b-alert>

    <b-table striped hover :busy="isLoading" :items="functions" :fields="fields">
      <template v-slot:table-busy>
        <div class="text-center text-danger my-2">
          <b-spinner class="align-middle"></b-spinner>
          <strong>Loading...</strong>
        </div>
      </template>

      <template v-slot:cell(actions)="row">
        <b-button
         variant="outline-primary"
         size="sm"
         @click="run(row.item, row.index, $event.target)"
         class="mr-1"
         >
          Run Function
        </b-button>
        <b-button size="sm" @click="info(row.item, row.index, $event.target)" class="mr-1">
          View Logs
        </b-button>
      </template>
    </b-table>

    <!-- Run modal -->
    <b-modal :id="runModal.id" :title="runModal.title" @ok="executeFunction" @hide="resetRunModal">
      <b-form-group label-cols="4" label-cols-lg="2" label="Name" label-for="runModal.name">
        <b-form-input disabled :value="runModal.name"></b-form-input>
      </b-form-group>
      <b-form-group label-cols="4" label-cols-lg="2" label="Argument" label-for="runModal.args">
        <b-form-input v-model="argument.key" placeholder="key"></b-form-input>
        <b-form-input v-model="argument.val" placeholder="value"></b-form-input>
      </b-form-group>
    </b-modal>

    <!-- Info modal -->
    <b-modal :id="infoModal.id" :title="infoModal.title" ok-only @hide="resetInfoModal">
      <pre>{{ infoModal.content }}</pre>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
/* eslint-disable */
export default {
  name: 'Table',
  data() {
    this.fetch_data();
    return {
      isLoading: true,
      functions: [
      ],
      fields: [
        {
          key: 'name', label: 'Name',
        },
        {
          key: 'timestamp', label: 'Timestamp',
        },
        {
          key: 'func_name', label: 'Function Name',
        },
        {
          key: 'content', label: 'Content',
        },
        {
          key: 'dependencies', label: 'Dependencies',
        },
        { key: 'actions', label: 'Actions' },
      ],
      infoModal: {
        id: 'info-modal',
        title: '',
        content: '',
      },
      runModal: {
        id: 'run-modal',
        title: '',
        name: '',
        args: '',
      },
      argument: {
        key: '',
        val: '',
      },
      variant: 'primary',
      shouldShowAlert: false,
      alertMessage: '',
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
    info(item, index, button) {
      this.infoModal.title = `Previous Logs for: ${item.name}`;
      axios.get(`http://localhost:3000/logs?name=${item.name}`)
        .then((response) => {
          this.infoModal.content = JSON.stringify(response.data, null, 2);
          this.$root.$emit('bv::show::modal', this.infoModal.id, button);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    run(item, index, button) {
      this.runModal.title = `Run ${item.name}`;
      this.runModal.name = item.name;
      this.$root.$emit('bv::show::modal', this.runModal.id, button);
    },
    resetInfoModal() {
      this.infoModal.title = '';
      this.infoModal.content = '';
    },
    resetRunModal() {
      this.runModal.title = '';
      this.runModal.args = '';
      this.argument.key = '';
      this.argument.val = '';
    },
    executeFunction() {
      let combined = {'name': this.runModal.name};
      combined.args = {}
      if (this.argument.key && this.argument.val) {
        combined.args[this.argument.key] = this.argument.val;
      }

      console.log(combined);
      axios.post(`http://localhost:5000/run`, combined)
        .then((response) => {
          this.variant = 'success';
          this.alertMessage = `Successfully ran the function ${this.runModal.name}. Click 'View Logs' to see the output.`;
          this.shouldShowAlert = true;
          console.log(response)
        })
        .catch((error) => {
          this.variant = 'danger';
          this.alertMessage = `Something went wrong running the function ${this.runModal.name}. Check the console for errors.`;
          this.shouldShowAlert = true;
          console.log(error);
        });
    },
  },
};
</script>
