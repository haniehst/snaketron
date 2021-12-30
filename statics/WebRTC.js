var localVideo;
var remoteVideo;
var socket;
var peerConnection;
var uuid;
var isCaller;

var peerConnectionConfig = {
	'iceServers': [
		{'urls': 'stun.l.google.com:19302'},
		{'urls': 'stun.stunprotocol.org:3478'},
		{
			url: 'turn:relay.backups.cz',
			credential: 'webrtc',
			username: 'webrtc'
		}
	]
};

var constraints = {
	video:true,
	audio:true
};


function init_chat(sock,Caller) {
	socket = sock;
	isCaller = Caller;
	uuid = uuid();
	start();
}


function sendbySocket(json, type){
	socket.emit(type, json);
}


function start() {
	localVideo = document.getElementById('localVideo');
	remoteVideo = document.getElementById('remoteVideo');

	peerConnection = new RTCPeerConnection(peerConnectionConfig);
	peerConnection.onaddstream = gotRemoteStream;
	peerConnection.onicecandidate = gotIceCandidate;    
	peerConnection.ontrack = gotRemoteStream;

	if(navigator.mediaDevices.getUserMedia) {
		navigator.mediaDevices.getUserMedia(constraints).then(getUserMediaSuccess).catch(errorHandler);
	}
	else {
		alert('Your browser does not support getUserMedia API');
	}
}


function getUserMediaSuccess(stream) {
	console.log("getUserMediaSuccess");
	localStream = stream;
	localVideo.src = window.URL.createObjectURL(stream);
	peerConnection.addStream(localStream);
	

	if(isCaller){
		peerConnection.createOffer().then(createdDescription).catch(errorHandler);
	}
}


function gotIceCandidate(event) {
	if(event.candidate != null)
		sendbySocket(JSON.stringify({'ice': event.candidate, 'uuid': uuid, "room":"{{name}}"}), "ice");
}


function gotRemoteStream(event) {
	console.log('gotRemoteStreamSuccess');
	remoteVideo.src = window.URL.createObjectURL(event.stream);
}


function createdDescription(description) {
	peerConnection.setLocalDescription(description).then(function() {
		sendbySocket(JSON.stringify({'sdp': peerConnection.localDescription, 'uuid': uuid, "room":"{{name}}"}), 'sdp');
	}).catch(errorHandler);
}


function errorHandler(error) {
	console.log(error);
}


function uuid() {
	function s4() {
		return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
	}
	return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
}


console.log('webrtc.js');
