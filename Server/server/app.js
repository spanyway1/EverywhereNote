var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var myroute = require('./routes/myroute.js');
  
var app = express();
//Express를 기반으로 서버를 구축하였습니다.

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

//file 처리를 위한 라우터 등록
app.use('/file', myroute);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
// set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = process.env.NODE_ENV === 'development' ? err : {};
  // render the error page
  res.status(err.status || 500);
});

module.exports = app;