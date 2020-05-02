const express = require('express');
const router = express.Router()
const userAuth = require('../DBConnection/auth')

router.post('/',userAuth.test)
router.get('/all-report',userAuth.getAllReport)

router.post('/register',userAuth.userAuth)

router.post('/login',userAuth.loginAuth)


module.exports = router;