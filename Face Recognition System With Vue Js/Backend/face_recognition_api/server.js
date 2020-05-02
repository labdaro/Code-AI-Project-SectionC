const express = require('express');
const bodyParser = require('body-parser');
const Joi  = require('joi');
const app = express();
const cors = require('cors')

app.use(cors())
app.use(bodyParser.json());
app.use( bodyParser.urlencoded({extended: true}));

//Get the connection to the database and do operation
const db = require('./DBConnection/db')

//get all the routers
app.use('/',require('./routes/Routers'))


const PORT = process.env.PORT || 5000;
app.listen(PORT,()=>console.log(`Server is listen on port:${PORT}`));