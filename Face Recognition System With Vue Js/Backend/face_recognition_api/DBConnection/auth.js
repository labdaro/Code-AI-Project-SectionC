const Joi = require('joi')
const express =require('express')
const app = express()
const dotenv = require('dotenv')
const jwt = require('jsonwebtoken')
const bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use( bodyParser.urlencoded({extended: true}));

dotenv.config();
const {Pool} = require('pg');
const bcrypt = require('bcryptjs')
const pool = new Pool({
    user: process.env.DB_USER,
    password:process.env.DB_PASSWORD,
    host:process.env.DB_HOST,
    database: process.env.DB_DATABASE
});
  const test = async (request,response)=>{
    console.log(request.body)
      response.send(request.body)
  }
  //register the user
  const userAuth = async (request, response) => {
    const {report_id,fullname,username} = request.body
    const salt = await bcrypt.genSalt(10);
    const hashPassword = await bcrypt.hash(request.body.password,salt)

    pool.query('SELECT username FROM users where username =$1',[username], (error, results) => {

      //check is the username is already exist  
      if(Object.entries(results.rows).length === 0){
              const schema ={
                 report_id: Joi.required(),
                 fullname: Joi.string().min(6).required(),
                 username: Joi.string().min(6).required(),
                 password: Joi.string().min(6).required()
              }
              const {error} = Joi.validate(request.body,schema);
              if(error){
                 response.json({
                   data: error.details[0].message,
                  validateCode: false
                  })
                // console.log(error.details[0].message)
                // response.send(error.details[0].message);
              }
              else{
                try {
                  pool.query('insert into users (report_id,fullname,username,password) VALUES ($1, $2,$3,$4)', [report_id,fullname,username,hashPassword], (error, results) => {
                  if (error) {  
                    throw error
                    }
                    response.status(200).json({
                      data:"Register Successfully...",
                      validateCode: true
                    }
                    )
                  })
              }catch (err) {
                  response.send(err)
              }
            }
          }else{
            response.json({
              data:"username is already exist...",
              validateCode: false
            })
         }     
    })
};


const loginAuth = async (request,response) =>{
      const {username,password} = request.body
      pool.query('select report_id,username,password from users where username=$1',[username],(error,results)=>{
        if(Object.entries(results.rows).length === 0){
          response.send('Username is incorrect...')      
        }
         if (Object.entries(results.rows).length != 0){
           // check password from database 
            const hashPass = results.rows[0].password
            //get id from database 
            const id = results.rows[0].report_id

            bcrypt.compare(request.body.password,hashPass,(err,isMatch)=>{
              if(!isMatch){
                response.send('Password is incorrect...')
              }else{
                response.sendStatus(200).send()
              }
            })
        }
      })

    }


    const getAllReport = async (request,response) =>{
      pool.query('select * from report',(error,results)=>{
        response.json(results.rows)
      })
     
    }
    
module.exports = {userAuth,loginAuth,getAllReport,test}