/*mapkey = 'AIzaSyCYgEd0pvpaEYYHzI1fVZrrLSrg1Pvsy14'


var geocoder = new google.maps.Geocoder();
var address = document.getElementById("address").value;
//console.log(address)

//geocoder.geocode(address, key=mapkey, function(results, status) {
geocoder.geocode({'address':address},function(results,status){  
console.log("here")
if (status == google.maps.GeocoderStatus.OK) {
    var latitude = results[0].geometry.location.lat();
    var longitude = results[0].geometry.location.lng();
    alert(latitude);
    } 
else { console.log(status)}
}); */
//from geopy.geocoders import Nominatim;


var add = document.getElementById("address").value
var house = document.getElementById("houseArea").value
var plot = document.getElementById("plotArea").value
var year = document.getElementById("houseArea").value
var bed = document.getElementById("beds").value
var baths = document.getElementById("baths").value
var tax = document.getElementById("taxA").value
var zip = document.getElementById("zip").value
//console.log(house)


function updatePrices(){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/getLREGValue"); 
    xhr.onload = function(event){ 
        //alert("Success, server responded with: " + event.target.response); // raw response
        document.getElementById("lreg").innerHTML = "<h2>"+event.target.response+"</h2>";
    }; 
    // or onerror, onabort
    var formData = new FormData(document.getElementById("myForm")); 
    xhr.send(formData);

    var xhr2 = new XMLHttpRequest();
    xhr2.open("POST", "/getSVMValue"); 
    xhr2.onload = function(event){ 
        //alert("Success, server responded with: " + event.target.response); // raw response
        //document.getElementById("kmean").innerHTML = "<img src='./Images/Image.png'>";
        console.log(event.target.response)
    }; 
    // or onerror, onabort
    //var formData2 = new FormData(document.getElementById("myForm")); 
    xhr2.send(formData);
    //console.log("here")
}
updatePrices()