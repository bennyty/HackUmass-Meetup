// app/models/user.html
var mongoose = require('mongoose');
var bcrypt = require('bcrypt-nodejs');


var userSchema = mongoose.Schema({
  //email based authentication
  email:{
    email: String,
    password: String,
  },
  //google based authentication
  google:{
    id: String,
    toke: String,
    email: String,
    name: String
  }
})

//create hash of pw
userSchema.methods.generateHash = function(password){
  return bcrypt.hashSync(password, bcrypt.genSaltSync(10), null);
}

//checks given hash from user
userSchema.methods.validPassword = function(password){
  return bcrypt.compareSync(password, this.local.password);
}

module.exports = mongoose.model('User', userSchema);
