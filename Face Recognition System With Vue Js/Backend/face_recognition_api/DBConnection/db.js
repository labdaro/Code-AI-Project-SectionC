// const Joi = require('joi')
// const dotenv = require('dotenv')
// const jwt = require('jsonwebtoken')
// const uuid = require('uuid')
// dotenv.config();
// const {Pool} = require('pg');
// const bcrypt = require('bcryptjs')
// const pool = new Pool({
//     user: process.env.DB_USER,
//     password:process.env.DB_PASSWORD,
//     host:process.env.DB_HOST,
//     database: process.env.DB_DATABASE
// });


// const getAllReport = async (request,response) =>{
//   pool.query('select * from report',(error,results)=>{
//     response.json(results.rows)
//   })
// }

// module.exports = {getAllReport}