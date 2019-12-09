const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const bodyParser = require('body-parser');
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

app.get('/ping/', (req, res) => {
  res.send('pong');
});

app.post('/create', (req, res) => {
  const func = req.body.function;
  const dependencies = req.body.dependencies;
  const language = req.body.language;

  res.send(func + ' ' + dependencies + ' ' + language);
});


app.listen(port, () => console.log('We are live on Port:' + port));
