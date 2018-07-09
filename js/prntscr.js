// 1. Go to http://prntscr.com/gallery.html > load all images. Get images to imgCodes
var codes = [].slice.call(document.getElementsByClassName("gallery-item")).map((el) => el.getAttribute("data-id36"));

// 2. Go to prntscr-snatcher App. Use the app to get the imgurCodes
var imgurCodes = [];
for (var i=imgCodes.length-1; i>=0; i--){
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function(){
		if (xhttp.readyState == 4 && xhttp.status == 200){
			if (xhttp.responseText){
				imgurCodes[i] = xhttp.responseText;
			}
		}
	};
	xhttp.open("GET", "imgCode/" + imgCodes[i], true);
	xhttp.send();
}

// 3. wget the links. voila
