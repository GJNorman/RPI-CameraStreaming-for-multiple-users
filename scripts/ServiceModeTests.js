/**
window.location.href is the server IP + Port address
**/

//set new coordiantes for selected ROI; without permanentely saving to file
function setROIValues(){
	sendBasicPostRequest(window.location.href + '/setROI?ROIName=EXAMPLE_ROI_1&top=25&bottom=35&left=30&right=40&Colour=red');
}
//return to application mode
function enterApplicationMode(){
	sendBasicPostRequest(window.location.href + '/applicationMode');
}
//save current ROI settings to file
function saveROISettings(){
	sendBasicPostRequest(window.location.href + '/saveROIs');
}
//get width and height of the camera stream
function checkImageDimensions()
{	
	var img = document.getElementById('cameraStream'); 

	console.log(img.clientWidth,img.clientHeight);
	
	return [img.clientWidth,img.clientHeight]
}
//this function is called once the program has entered service mode
//it will process the list of recieved ROI boundaries via "Http.responseText"
function processROIBoundaries(Http){
	console.log(Http.responseText)		//this contains the information about regions of interest
}
//tell the program to enter service mode 
function setServicemode(){
	sendGetRequest(window.location.href + '/serviceMode',"text",processROIBoundaries);
}

// enter service mode when the user clicks ont the 'service-mode-button'
document.getElementById("Service-Mode-button").addEventListener('click', setServicemode);

//disable image dragging
document.getElementById('cameraStream').ondragstart = function() { return false; };

//detect click coordinates
document.getElementById("cameraStream").addEventListener("click",  e => 
{
	var dims=checkImageDimensions();
	console.log(e.clientY,e.clientX,dims[0],dims[1]);
})
