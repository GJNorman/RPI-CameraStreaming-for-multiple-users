
/*
	example usage

      function sum(x, y, z) {
        console.log(x+y+z)
      }

      sendGetRequest(window.location.href + '/someValue',sum,1,2,3)

      output : 6
*/
function sendGetRequest(URL, responseType,callback,...callbackArgs){
	const Http = new XMLHttpRequest();
	Http.responseType = responseType;
	Http.open("GET",URL);
	Http.send();
	Http.onload=(e)=>{
		callback(Http,...callbackArgs);
	}
}

// 	example use 
//	sendBasicPostRequest(window.location.href + '/someValue')
function sendBasicPostRequest(URL){
        const Http = new XMLHttpRequest();
        Http.open("POST",URL);
        Http.send();
}

// basic timer
// var myTimer = new Timer(timeinmilliseconds);
// while (true) {
//	if(myTimer.checkTimeout() == true){
//		//do something
//	}
class Timer{
	constructor(timeoutPeriod_ms,optionalCallback){
		this.startTime = this.currentTime();
		this.timeout = timeoutPeriod_ms;
		this.callback = null;
		if (typeof (optionalCallback) != undefined)
			this.callback = optionalCallback
	}
	setTimeout(timeoutPeriod_ms){
		this.timeout = timeoutPeriod_ms;
	}
	setCallback(newCallback){
		this.callback = newCallback;
	}
	updateReferenceTime(){
		this.startTime = this.currentTime();
	}
 	currentTime(){
		return Date.now();
	}
	checkTimout(){
		if(this.currentTime() - this.startTime	>= this.timeout){
			this.updateReferenceTime();
			if (this.callback != null)
				this.callback();
			return true;
		}
		return false;
	}
}

//doubling clicking certain buttons will bugger erything right up; so we'll add a cooldown to avoid it
//
//	function exampleCallback(someArgument){
//		doSomething(someArgument)
//	}
//	var myButton = new buttonCoolDownTimer(timeInMilliSeconds);
//
//	function buttonCallback(){
//		var someArgument = 7;
//		myButton.useButton(exampleCallback,someArgument);
//	}
class buttonCoolDownTimer{
	constructor(cooldownPeriod_ms){
		this.Timer = new Timer(cooldownPeriod_ms);
		this.firstTimeUse = true;			//avoid cooldown on loading webpage
	}	
	// Getters
	useButton(callback,...args){
		if ((this.Timer.checkTimout() == true) || (this.firstTimeUse==true)){
			this.firstTimeUse = false;
			callback(args);
		}
	}
}
	
