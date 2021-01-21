import React from "react";;
import {STATIC_URL} from "../../helpers/env.js";

export class LexClass extends React.Component {

    componentDidMount() {
        var waveform = window.Waveform();
        var message = document.getElementById('message');
        var config, conversation;
        message.textContent = 'Passive';

        document.getElementById('audio-control').onclick = function () {

            AWS.config.credentials = new AWS.Credentials(document.getElementById('ACCESS_ID').value, document.getElementById('SECRET_KEY').value, null);
            AWS.config.region = 'us-east-1';
            
            config = {
                lexConfig: { botName: document.getElementById('BOT').value }
            };

            conversation = new LexAudio.conversation(config, function (state) {
                message.textContent = state + '...';
                if (state === 'Listening') {
                    waveform.prepCanvas();
                }
                if (state === 'Sending') {
                    waveform.clearCanvas();
                }
            }, function (data) {
                console.log('Transcript: ', data.inputTranscript, ", Response: ", data.message);
            }, function (error) {
                message.textContent = error;
            }, function (timeDomain, bufferLength) {
                waveform.visualizeAudioBuffer(timeDomain, bufferLength);
            });
            conversation.advanceConversation();
        };

        document.getElementById('pauseLex').onclick = function () {
        //     // AWS.config.credentials = new AWS.Credentials(document.getElementById('ACCESS_ID').value, document.getElementById('SECRET_KEY').value, null);
        //     // AWS.config.region = 'us-east-1';
            
        //     // config = {
        //     //     lexConfig: { botName: document.getElementById('BOT').value }
        //     // };

        //     // conversation = new LexAudio.conversation(config, function (state) {
        //     //     message.textContent = 'Passive';
        //     // });
        //     // conversation.advanceConversation();
        //     // conversation.reset();
        //     // document.getElementById("message").innerHTML = "Passive"; 
            window.location.reload();
        //     // global.LexAudio.audioControl.stopRecording();
        //     // global.LexAudio.audioControl.clear();
        //     // var audioControl = new LexAudio.audioControl();
        //     // audioControl.stopRecording();

        }
    }
  
    render() {
      
      return (
		 <div>
             <div style={{fontWeight:600, marginTop: 8,top: 80,left:105,position:"absolute"}}>Please Click on the below icon to trigger model creation :</div>
              <button className="lexBtn" id="pauseLex">
               <span class="glyphicon glyphicon-refresh" style={{paddingRight:5}}></span>Reset
              </button> 
              <div className="audio-control">
                <p id="audio-control" className="white-circle">
                    <img style={{height:55,marginTop:6}} src= { STATIC_URL + "assets/images/LexIcon.png"} />
                    <canvas className="visualizer"></canvas>
                </p>
                <p><span id="message"></span></p>
                <div className="noDisplay">
                <p>
                    <input type="password" id="ACCESS_ID" name="ACCESS ID" placeholder="ACCESS ID" value="AKIAVIZ5TXPQHRHOCK44"/>
                </p>
                <p>
                    <input type="password" id="SECRET_KEY" name="SECRET KEY" placeholder="SECRET KEY" value="K2AgBNvRCpW6EYF4QsR2vP4EDDGHpbt6fiVCVpvh"/>
                </p>
                <input type="text" id="BOT" name="BOT" placeholder="BOT" value="mBot" />
                </div>
            </div>
            </div>
        )


    }



}
