const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const fs = require('fs')
const util = require('util')
const axios = require('axios');

const port = process.env.PORT || 3000;

const app = express();

app.use(express.json());
app.use(morgan('dev'));
app.use(cors());
app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies

app.get('/', (req, res) => {
  res.send('Welcome to ProtoK.');
});

app.get('/get_all', (req, res) => {

  axios.get('http://10.145.196.253:5000/get_all')
  .then((response) => {

    try {
      let items = response.data[Object.keys(response.data)[0]].items;
      let result = [];

      for (let i = 0; i < items.length; i++) {
        const entry = items[i];
        let tmpToReturn = {};
        if (entry.metadata) {
          if (entry.metadata.name) {
            tmpToReturn['name'] = entry.metadata.name;
          }
          if (entry.metadata.creationTimestamp) {
            tmpToReturn['timestamp'] = entry.metadata.creationTimestamp;
          }
        }
        if (entry.spec) {
          if (entry.spec.target_function) {
            tmpToReturn['func_name'] = entry.spec.target_function;
          }
          if (entry.spec.content) {
            tmpToReturn['content'] = entry.spec.content;
          }
          if (entry.spec.dependencies) {
            tmpToReturn['dependencies'] = entry.spec.dependencies;
          }
        }
        result.push(tmpToReturn);
      }

      res.send(result);
    } catch (error) {
      res.send(error);
    }
  })
  .catch((error) => {
    console.log(error);
    res.send(error);
  });
});

app.listen(port, () => console.log('We are live on Port:' + port));
