var start = 1970;
var end = new Date().getFullYear();
//var options = "<option>Before 1970</option>";
var options = ""
for(var year = start ; year <=end; year++){
  options += "<option>"+ year +"</option>";
}
document.getElementById("year").innerHTML = options;

options = "";
for(var i = 0 ; i <=10; i++){
    options += "<option>"+ i +"</option>";
}
document.getElementById("beds").innerHTML = options;
document.getElementById("baths").innerHTML = options;

options = "";
for(var foot = 500;foot<=12000;foot+=100){
    options += "<option>"+foot+"</option>";
}
document.getElementById("houseArea").innerHTML=options;


options = "";
for(var plot = 1;plot<=500;plot++){
    options += "<option>"+plot+"</option>";
}
document.getElementById("plotArea").innerHTML=options;

options = "";
for(var tax = 1000;tax<=300000;tax+=100){
    options += "<option>"+tax+"</option>";
}
document.getElementById("taxA").innerHTML=options;
/*
options = "";
for(var last = 1000;last<=300000;last+=100){
    options += "<option>"+last+"</option>";
}
document.getElementById("lastSold").innerHTML=options;*/