var eduRegex = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.[Ee][Dd][Uu]$/;

function validateForm() {
    var x = document.forms.login.email.value;

    if ((x === null) || (x === "")){
        swal("", "Please fill in your email address.", "error");
        return false;
    }
    var exists = eduRegex.test(x);
    
    if (exists === false){
      swal("", "Please use your '.edu' email address to log in.", "warning");
    }
  
    return exists;
}