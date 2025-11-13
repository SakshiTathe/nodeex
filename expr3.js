const mongoose = require('mongoose');
const http=require('http');

const mongoURI = 'mongodb://127.0.0.1:27017/exp1'; 

mongoose.connect(mongoURI)
.then(() => console.log('MongoDB connected successfully'))
.catch(err => console.error('MongoDB connection error:', err));

const server=http.createServer((req,res)=>{
    res.end('Hello, World from Node.js Server!');
})
server.listen(3000,"localhost",()=>{
    console.log("server is started")
})