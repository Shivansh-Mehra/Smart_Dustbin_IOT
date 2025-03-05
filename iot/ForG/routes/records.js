const express = require('express');
const router = express.Router();
const User = require('../models/user');
// const Contractor = require('../models/contractor');

router.get('/users', async (req, res) => {
  try {
    const users = await User.find();
    res.render('users', { users });
  } catch (err) {
    res.status(500).send(err.message);
  }
});



module.exports = router;