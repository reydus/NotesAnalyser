const bars = 4096

class AudioVisualizer {
  constructor(audioContext, processFrame, processError) {
    this.audioContext = audioContext;
    this.processFrame = processFrame;
    this.connectStream = this.connectStream.bind(this);
    navigator.mediaDevices.getUserMedia({ audio: true, video: false }).
    then(this.connectStream).
    catch(error => {
      if (processError) {
        processError(error);
      }
    });
  }

  connectStream(stream) {
    this.analyser = this.audioContext.createAnalyser();
    const source = this.audioContext.createMediaStreamSource(stream);
    source.connect(this.analyser);
    this.analyser.smoothingTimeConstant = 0.5;
    this.analyser.fftSize = bars;

    this.initRenderLoop(this.analyser);
  }

  initRenderLoop() {
    const frequencyData = new Uint8Array(this.analyser.frequencyBinCount);
    const processFrame = this.processFrame || (() => {});

    const renderFrame = () => {
      this.analyser.getByteFrequencyData(frequencyData);
      processFrame(frequencyData);

      requestAnimationFrame(renderFrame);
    };
    requestAnimationFrame(renderFrame);
  }}


const visualMainElement = document.querySelector('main');
//const visualValueCount = bars / 2;
// let visualElements;
const createDOMElements = () => {
  let i;
  for (i = 0; i < visualValueCount; ++i) {
    const elm = document.createElement('div');
    visualMainElement.appendChild(elm);
  }

  visualElements = document.querySelectorAll('main div');
};
//createDOMElements();

const init = () => {
  // Creating initial DOM elements
  const audioContext = new AudioContext({sampleRate: 48000}); // Incoming stream AudioNode is 48kHz, cannot connect different rates. Decimate?
  console.log("Current sampling frequency is "+String(audioContext.sampleRate));
  const initDOM = () => {
    var but = document.getElementById("startbutton");
    but.parentNode.removeChild(but);
    //visualMainElement.innerHTML = '';
    //createDOMElements();
  };
  initDOM();

  // Swapping values around for a better visual effect
  const dataMap = { 0: 15, 1: 10, 2: 8, 3: 9, 4: 6, 5: 5, 6: 2, 7: 1, 8: 0, 9: 4, 10: 3, 11: 7, 12: 11, 13: 12, 14: 13, 15: 14 };
  const processFrame = data => {
    const values = Object.values(data);
    let i;
    let dataSum = 0;
    const value = values[i] / 255;
    
    const A4 = 440;
    for (i = 0; i < values.length; ++i) {
      dataSum += values[i];
    }
    let dataAve = dataSum / values.length;
    // get frequency notes:


    /* for (i = 0; i < visualValueCount; ++i) {
      
      const value = values[i] / 255; //values[dataMap[i]] / 255;
      const elmStyles = visualElements[i].style;
      elmStyles.transform = `scaleY( ${value} )`;
      elmStyles.opacity = Math.max(.25, value);
    } */
    let maxFreq = values.indexOf(Math.max(...values)) / ((bars / 2) -1) * 24000


    const keyCi = document.getElementById("keyCi");
    const keyBbi = document.getElementById("keyBbi");
    const keyBi = document.getElementById("keyBi");
    const keyAi = document.getElementById("keyAi");
    const keyGi = document.getElementById("keyGi");
    const keyGsi = document.getElementById("keyGsi");
    const spatulaBbi = document.getElementById("spatulaBbi");
    const keyFi = document.getElementById("keyFi");
    const trill1i = document.getElementById("trill1i");
    const keyEi = document.getElementById("keyEi");
    const trill2i = document.getElementById("trill2i");
    const keyDi = document.getElementById("keyDi")
    const keyDsi = document.getElementById("keyDsi");
    const keyCsi = document.getElementById("keyCsi");
    const keyLowC = document.getElementById("keyLowCi");
    
    const order = [keyCi, keyBbi, keyBi, keyAi, keyGi, keyGsi, spatulaBbi, keyFi, trill1i, keyEi, trill2i, keyDi, keyDsi, keyCsi, keyLowC]
    
    const notes = {
      "C4": [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1],
      "Cs4": [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
      "D4": [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
      "Ds4": [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0],
      "E4": [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
      "F4": [1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
      "Fs4": [1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
      "G4": [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      "Gs4": [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      "A4": [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      "As4": [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
      "B4": [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      "C5": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      "Cs5": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      "D5": [0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
      "Ds5": [0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0],
      "E5": [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
      "F5": [1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
      "Fs5": [1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
      "G5": [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      "Gs5": [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      "A5": [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      "As5": [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
      "B5": [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      "C6": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      "Cs6": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      "D6": [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      "Ds6": [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0],
      "E6": [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      "F6": [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
      "Fs6": [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
      "G6": [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
    const pressed = "fill:#07c69c;fill-rule:evenodd;stroke:none;stroke-width:1.08509;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;fill-opacity:1"
    const unpressed = "fill:none;stroke:none;stroke-width:1.00357;stroke-linecap:butt;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"

    const notesSelection = ["C4", "Cs4", "D4", "Ds4", "E4", "F4", "Fs4", "G4", "Gs4", "A4", "As4", 
    "B4", "C5", "Cs5", "D5", "Ds5", "E5", "F5", "Fs5", "G5", "Gs5", "A5", "As5", "B5", "C6", "Cs6", "D6", "Ds6", "E6", "F6", "Fs6", "G6"];

    const noSharps = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5", "B5", "C6", "D6", "E6", "F6", "G6"]

    if (maxFreq >= 200 && maxFreq <= 1600 && dataAve > 2.3) {
      semiStepsOffset = Math.round(Math.log(maxFreq / A4) / Math.log(2) * 12);
      const note = notesSelection[semiStepsOffset+9]; // A4 is the tenth pitch playable in order for a C-foot flute.
      console.log("Max freq is: "+maxFreq+" offset in semi-steps is "+semiStepsOffset+" and note is "+note);
      
      if (note != undefined) {

        document.getElementById("highA").style["opacity"] = 0;
        document.getElementById("highC").style["opacity"] = 0;
        document.getElementById("highE").style["opacity"] = 0;
        document.getElementById("highG").style["opacity"] = 0;
        document.getElementById("lowC").style["opacity"] = 0;
        let i;
        for (i = 0; i < notes[note].length; i++) {
          (notes[note][i] == 1 ? order[i].style=pressed : order[i].style=unpressed);
        }

        let noteNatural = note.replace("s","");
        let verticalOffsetNote = parseInt(noSharps.indexOf(noteNatural) - noSharps.indexOf("A4")) * -2.83 + 4.675;
        document.getElementById("pitch").setAttribute("transform", "translate(0,"+verticalOffsetNote+")");

        if (note.includes("s")) {
          document.getElementById("sharp").style["opacity"] = 1;
        }else{
          document.getElementById("sharp").style["opacity"] = 0;
        }

        if ( parseInt(noSharps.indexOf(noteNatural) - noSharps.indexOf("A4")) < -4) {
          document.getElementById("lowC").style["opacity"] = 1;
        } 
        if (parseInt(noSharps.indexOf(noteNatural) - noSharps.indexOf("A4")) > 6) {
          document.getElementById("highA").style["opacity"] = 1;
        } 
        if (parseInt(noSharps.indexOf(noteNatural) - noSharps.indexOf("A4")) > 8) {
          document.getElementById("highC").style["opacity"] = 1;
        } 
        if (parseInt(noSharps.indexOf(noteNatural) - noSharps.indexOf("A4")) > 10) {
          document.getElementById("highE").style["opacity"] = 1;
        } 
        if (parseInt(noSharps.indexOf(noteNatural) - noSharps.indexOf("A4")) > 12) {
          document.getElementById("highG").style["opacity"] = 1;
        } 


        document.getElementById("note_string").innerHTML = note;

    }
    }else{
      console.log("Max freq is: "+maxFreq);
    }
    


    console.log(dataAve);
  };

  const processError = () => {
    visualMainElement.classList.add('error');
    visualMainElement.innerText = 'Please allow access to your microphone in order to see this demo.\nNothing bad is going to happen... hopefully :P';
  };

  const a = new AudioVisualizer(audioContext, processFrame, processError);
};