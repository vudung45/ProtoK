<template>
  <div class="hello">
    <b-table striped hover :busy="isLoading" :items="functions" :fields="fields">
      <template v-slot:table-busy>
        <div class="text-center text-danger my-2">
          <b-spinner class="align-middle"></b-spinner>
          <strong>Loading...</strong>
        </div>
      </template>

      <template v-slot:cell(actions)="row">
        <b-button size="sm" @click="info(row.item, row.index, $event.target)" class="mr-1">
          View Logs
        </b-button>
      </template>
    </b-table>

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
    resetInfoModal() {
      this.infoModal.title = '';
      this.infoModal.content = '';
    },
  },
};
</script>
