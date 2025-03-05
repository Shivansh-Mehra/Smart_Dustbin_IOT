const express = require('express');
const router = express.Router();
const axios = require('axios');

const User = require('../models/user');
// const Contractor = require('../models/contractor');
const bcrypt = require('bcrypt');

// Home page route
router.get('/', (req, res) => {
  res.render('index', { title: 'Garbage Segragator IOT Project' });
});

// Registration form route
router.get('/register', (req, res) => {
  res.render('register'); 
});

// Registration route
router.post('/register', async (req, res) => {
  const { name, email, password } = req.body;
  const hashedPassword = await bcrypt.hash(password, 10);

  // if (role === 'farmer') {
    const us = new User({ name, email, password: hashedPassword });
    await us.save();

  res.redirect('/login');
});

router.get('/login', (req, res) => {
  res.render('login');
});
router.get('/loader', (req, res) => {
  res.render('loader');
});
router.get('/result', (req, res) => {
  res.render('result');
});
router.post('/login', async (req, res) => {
  const { email, password } = req.body;

  let user;
 
    user = await User.findOne({ email });
  

  if (user && await bcrypt.compare(password, user.password)) {
    req.session.user = user;
    res.redirect('/profile');
  } else {
    res.redirect('/login');
  }
});

router.get('/profile', (req, res) => {
  if (!req.session.user) {
    return res.redirect('/login');
  }

  res.render('profile', { user: req.session.user });
});
// const axios = require('axios');
router.get('/predict', async (req, res) => {
  try {
      // Replace with your Flask server's URL
      const flaskUrl = 'http://127.0.0.1:5000/predict';  
      const response = await axios.get(flaskUrl);

      // Assuming the Flask server returns JSON data like { points: 10, group: "Plastic" }
      const { points, group , confidence } = response.data;

      // Redirect to the /result page with points and group as query parameters
      res.redirect(`/result?points=${points}&group=${group}&confidence=${confidence}`);
  } catch (error) {
      console.error('Error fetching prediction from Flask:', error.message);
      res.status(500).json({ error: 'Error fetching prediction' });
  }
});


module.exports = router;