
var FPS = 20


function processNextFrame(Http, ImgID,NextTimeInterval)
{

	var fr = new FileReader();
	fr.onload = function(){
		document.getElementById(ImgID).src = this.result;
		
		//if(typeof NextTimeInterval !== "undefined") 
			setTimeout(GetNextFrame, NextTimeInterval)
	}
	fr.readAsDataURL(Http.response);
}
function GetNextFrame(){
	sendGetRequest(window.location.href + '/video_feed',"blob",processNextFrame,"cameraStream",1000/FPS)
}

function startFilming(){
	startFilmingButton.useButton(sendBasicPostRequest,window.location.href + '/startProcess'); 
 }
function stopFilming(){
	stopFilmingButton.useButton(sendBasicPostRequest,window.location.href + '/stopProcess');	
}

const startFilmingButton = new buttonCoolDownTimer(2000);
const stopFilmingButton = new buttonCoolDownTimer(2000);
setTimeout(GetNextFrame, 1000/FPS)
