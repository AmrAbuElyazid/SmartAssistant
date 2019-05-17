import { Component, ViewChild } from '@angular/core';
import { NavController, Platform } from 'ionic-angular';
import { HttpClient } from '@angular/common/http';

import { trigger, style, animate, transition, state } from '@angular/animations';

import { SpeechRecognition } from '@ionic-native/speech-recognition';
import { TextToSpeech } from '@ionic-native/text-to-speech';
import SiriWave from 'siriwave/src/siriwave';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html',
  providers: [],
})
export class HomePage {

  listening: boolean = false;
  siriWave: any = {};
  myText: string;
  response: string;
  myTextEl: any;
  responseEl: any;

  constructor(public navCtrl: NavController,
    private speechRecognition: SpeechRecognition,
    private tts: TextToSpeech,
    private http: HttpClient,
    private platform: Platform
    ) {
  }

  ionViewDidLoad() {
    // this.getBackground();
    // this.speechRecognition.hasPermission()
    //   .then((hasPermission: boolean) => alert(hasPermission))

    // Request permissions
    this.platform.ready().then(() => {
      this.initElements();
      this.changeResponseText('Hello, How can I help you?');
    })
    // this.changeMyText('Hey');
    // setTimeout(() => {
    //   this.changeResponseText('Hello, How can I help you?');
    //   setTimeout(() => {
    //     this.changeMyText('How you doing?')
    //     setTimeout(() => {
    //       this.changeResponseText('I am fine thank you!')
    //     }, 2000)
    //   }, 2000)
    // }, 2000)
  }

  initElements() {
    this.myTextEl = document.getElementById('my-text');
    this.responseEl = document.getElementById('response');
  }

  changeMyText(str) {
    if(!this.myText) {
      this.myText = str;
      this.myTextEl.classList += ' fadeIn';
      return;
    }
    this.myTextEl.classList = 'my-text fadeOut';
    this.myText = str;
    setTimeout(() => {
      this.myTextEl.classList = 'my-text fadeIn';
    }, 500)
  }

  changeResponseText(str) {
    if(!this.response) {
      this.response = str;
      this.tts.speak(str)
      this.responseEl.classList += ' fadeIn';
      return;
    }
    this.responseEl.classList = 'response fadeOut';
    this.response = '';
    this.response = str;
    setTimeout(() => {
      this.responseEl.classList = 'response fadeIn';
      this.tts.speak(str)
    }, 500)
  }

  startListening() {
    // alert('aa');
    this.listening = true;
    this.initWave();
    var self = this;
    self.speechRecognition.startListening({showPopup: false})
      .subscribe(
        (matches: Array<string>) => {
          self.speechRecognition.stopListening();
          self.changeMyText(matches[0]);
          self.http.get('http://192.168.43.142:5000/' + matches[0]).subscribe((res: any) => {
            self.listening = false;
            self.hideWave();
            self.changeResponseText(res.text);
              // .then(() => console.log('Success'))
              // .catch((reason: any) => console.log(reason));
          }, err => {
            // alert(JSON.stringify(err));
            self.hideWave();
          })
          // alert(JSON.stringify(matches));
        },
        (onerror) => {
          // alert('error:' + onerror)
          self.listening = false;
          self.hideWave();
          self.speechRecognition.stopListening();
          self.speechRecognition.requestPermission()
            .then(
              () => console.log('Granted'),
              () => console.log('Denied')
            )
        }
      )
  }

  initWave() {
    let wave = document.createElement('div');
    wave.setAttribute('id', 'siri');
    let content = document.getElementById('wave');
    content.appendChild(wave);
    this.siriWave = new SiriWave({
      container: document.getElementById('siri'),
      width: window.innerWidth,
      height: 200,
      style: 'ios9'
    });
    this.siriWave.start();
  }

  hideWave() {
    this.siriWave.stop();
    document.getElementById('siri').remove();
  }
}
