const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const fs = require('fs')
const util = require('util')

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

  let combined_vals = {"function": func, "dependencies": dependencies, "language": language};

  try {
    let readF = fs.readFileSync('./temp.json', 'utf-8');
    let parsed = JSON.parse(readF);
    parsed.entries.push(combined_vals);
  
    fs.writeFile('./temp.json', JSON.stringify(parsed), function (err) {
  
    });
  } catch (error) {
    // This error thrown is likely because we tried parsing (converting to JSON) an empty file
    // In this case, we just create the correct json file with the new entry given
    let parsed = JSON.parse('{"entries":[]}');
    parsed.entries.push(combined_vals);

    fs.writeFile('./temp.json', JSON.stringify(parsed), function (err) {
  
    });
    console.log(error);
  }

  res.send(combined_vals);
});

app.get('/readdata', (req, res) => {

  try {
    let rawdata = fs.readFileSync('./temp.json');
    let parsed = JSON.parse(rawdata);
    res.send(parsed);
  } catch (error) {
    res.send("Unable to load data. Make sure that temp.json has data in it.");
  }

});

app.listen(port, () => console.log('We are live on Port:' + port));
