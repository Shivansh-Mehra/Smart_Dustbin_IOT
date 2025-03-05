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
  if (!req.session.user) {
    return res.redirect('/login'); // Redirect to login if session is missing
  }

  // Extract query params
  const { points, group, confidence } = req.query;

  // Render the result page
  res.render('result', { points, group, confidence });
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

router.get('/profile', async (req, res) => {
  if (!req.session.user) {
    return res.redirect('/login');
  }

  try {
    const email = req.session.user.email;
    const user = await User.findOne({ email });

    if (!user) {
      return res.status(404).send('User not found');
    }

    // Render profile.ejs with the latest user data
    res.render('profile', { user });
  } catch (error) {
    console.error('Error fetching user data:', error.message);
    res.status(500).send('Server error');
  }
});


router.get('/predict', async (req, res) => {
  if (!req.session.user) {
    return res.redirect('/login');
  }

  try {
    const flaskUrl = 'http://127.0.0.1:5000/predict';
    const response = await axios.get(flaskUrl);
    const { points, group, confidence } = response.data;

    // Update user points
    const email = req.session.user.email;
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    user.points = (user.points || 0) + points / 2;
    await user.save();

    // Send the points, group, and confidence as a JSON response
    res.json({ points, group, confidence });
  } catch (error) {
    console.error('Error fetching prediction:', error.message);
    res.status(500).json({ error: 'Error fetching prediction' });
  }
});





module.exports = router;