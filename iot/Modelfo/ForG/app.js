const express = require('express');
const path = require('path');
const axios = require('axios');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const session = require('express-session');
const mongoose = require('mongoose');

const indexRouter = require('./routes/index');
const usersRouter = require('./routes/users');
const recordsRouter = require('./routes/records');

const app = express();

// Connect to MongoDB
mongoose.connect('mongodb://localhost/iotdb', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', () => {
  console.log('Connected to MongoDB');
});

// Set view engine
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

// Middleware
app.use((req, res, next) => {
  res.setHeader('Cache-Control', 'no-store');
  next();
});

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
  secret: 'your-secret-key', 
  resave: false, 
  saveUninitialized: false, // Change to false to prevent uninitialized sessions from being saved
  cookie: { 
    maxAge: 30 * 60 * 1000, // Set cookie expiration (e.g., 30 minutes)
    httpOnly: true, // Prevents client-side JavaScript from accessing the cookie
    secure: false // Set to true if you're using HTTPS
  }
}));

// Check session middleware
const checkSession = (req, res, next) => {
  if (!req.session.user) {
    return res.redirect('/login'); // Redirect to login if session is invalid
  }
  next(); // Proceed to the next middleware/route handler
};

// Apply the check session middleware to specific routes
app.use('/predict', checkSession);
app.use('/users', checkSession);

// Routes
app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/records', recordsRouter);

// Catch 404 and forward to error handler
app.use((req, res, next) => {
  const err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// Error handler
app.use((err, req, res, next) => {
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};
  res.status(err.status || 500);
  res.render('error');
});

// Start server
const port = 3000;
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
