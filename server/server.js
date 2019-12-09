const express = require('express');
const cors = require('cors');
const port = process.env.PORT || 3000;

const app = express();

app.get('/', (req, res) => {
  res.send('Welcome to ProtoK.');
});

app.get('/ping/', cors(), (req, res) => {
  res.send('pong');
});

app.listen(port, () => console.log('We are live on Port:' + port));
