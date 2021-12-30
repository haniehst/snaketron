function SignallingChannel(id, isCaller, onmessage) {
	this.id = id;
	this.isCaller = isCaller;
	this.onmessage = onmessage;

	this.send = function(message) {
		if (this.isCaller)
			sendXHR(this.id, null, message);
		else
			sendXHR('caller_' + this.id, null, message);
	};

	if (this.isCaller)
		sendSSE('caller_' + this.id, this.onmessage);
	else
		sendSSE(this.id, this.onmessage);
}

function sendSSE(id, callback) {
	var source = new EventSource('/sse/' + id);
	source.onmessage = callback;
}

function sendXHR(id, callback, text) {
	var xhttp = new XMLHttpRequest();
	xhttp.onload = callback;
	xhttp.open("POST", "/xhr/" + id, true);
	xhttp.send(text);
}
