const express = require('express');
const app = express();
const bodyparser = require('body-parser');
const cors = require('cors');
const mongoose = require('mongoose');
const User = require('./model')
app.use(bodyparser.json());
app.use(cors());
const jwt = require('jsonwebtoken');
const JWT_SECRET = "your_secret_key";


mongoose.connect('mongodb://127.0.0.1:27017/exp1')
    .then(() => console.log('MongoDB connected successfully'))
    .catch(err => console.error('MongoDB connection error:', err));

let items = [
    { id: 1, name: 'Item 1' },
    { id: 2, name: 'Item 2' }
];

app.post('/api/items', (req, res) => {
    const { name } = req.body;
    const newitem = { id: items.length + 1, name };
    items.push(newitem);
    res.status(200).json(newitem);
})

app.get('/api/getitem', (req, res) => {
    res.json(items);
})
app.get('/api/getitem/:id', (req, res) => {
    const itemf = items.find(i => i.id === parseInt(req.params.id));
    if (!itemf) return res.status(404).send("item not found");
    res.json(itemf);
})
app.put('/api/upitem/:id', (req, res) => {
    const item = items.find(i => i.id === parseInt(req.params.id));
    if (!item) return res.status(404).send("item not found");
    item.name = req.body.name;
    res.json(item);
})

app.delete('/api/delitem/:id', (req, res) => {
    const itemind = items.findIndex(i => i.id === parseInt(req.params.id));
    if (itemind === -1) return res.status(404).send("item not found");
    const deleteditm = items.splice(itemind, 1);
    res.send(deleteditm);
})

app.post('/api/info', async (req, res) => {
    //const newitems=new User({username: req.body.username,password: req.body.password});
    //await newitems.save();
    const users = await User.insertMany(req.body);
    res.status(201).json(users);
})
app.post('/api/submitform', async (req, res) => {
    //const newitems=[new User({username: req.body.username,password: req.body.password})];
    //const findid=await User.findOne({username:newitems[0].username});
    /*if (newitems.password === findid.password) {
        res.status(201).redirect()
    }*/
    const { username, password } = req.body;
    const user = await User.findOne({ username });
    if (!user) return res.status(401).json({ success: false, message: "User not found" });


    const token= jwt.sign({
        userid:user._id},
        JWT_SECRET,
        {expiresIn:"1h"})
    if (user.password === password) {return res.json({ success: true, token });
        } else {
            return res.json({success:false});}
})

app.get('/', (req, res) => {
    res.send("Welcome to the Express.js Tutorial");
})


app.listen(3001, () => {
    console.log('Server is running on http://localhost');
})
