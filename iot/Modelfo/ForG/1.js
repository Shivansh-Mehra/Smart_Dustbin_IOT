const express = require('express');
const bp = require('body-parser');
const app = express();
const dotenv = require('dotenv').config();
const port  =process.env.PORT || 3000;
app.use(bp.json())

app.listen(port, ()=>{
     console.log('Makima is Watching');
     console.log(process.env.PORT);
})

app.get('/' , (req,res,next)=>{
    

     
});
