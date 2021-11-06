var midi = null;
var input_devices = [];
var output_devices = [];

//jquery読み込み
jQuery = $ = require('jquery');
//web midi使用
navigator.requestMIDIAccess().then(onMIDISuccess,onMIDIFailure);
function onMIDIFailure(msg){
    console.log("onMIDIFailure(): "+msg);
}
function onMIDISuccess(m){
    midi=m;
    //MIDI I/Oデバイス列挙
    var it = midi.inputs.values();
    for(var o = it.next(); !o.done; o = it.next()){
      input_devices.push(o.value);
    }
    var ot = midi.outputs.values();
    for(var o = ot.next(); !o.done; o = ot.next()){
      output_devices.push(o.value);
    }
    console.log(input_devices);
    console.log(output_devices);
}

//MIDIノート信号送信
function MidiNoteOn(note, vel){
    if(output_devices.length > 0){
        console.log("note on")
        output_devices[0].send([0x90,note,vel]);
        if($("#"+note.toString()).attr("class")=="piano_key"){
            $("#"+note.toString()).css("background-color","gray");
        }else{
            $("#"+note.toString()).css("background-color","dimgray");
        }
    }
}
//MIDIノートオフ信号送信
function MidiNoteOff(note){
    if(output_devices.length > 0){
        console.log("note off")
        output_devices[0].send([0x90,note,0x00]);
        $("#"+note.toString()).css("background-color","");
    }
}


var keys1 = ["q","w","e","r","t","y","u","i","o","P","@","["]
var keys2 = ["a","s","d","f","g","h","j","k","l",";",":","]"]
var keys3 = ["z","x","c","v","b","n","m",",",".","/","_"]
pressed_keys=[]
//文字のキー入力
document.addEventListener('keydown', (event) => {
    var keyName = event.key;
    console.log(keyName+" pressed");
    //文字キーが押されたときの反応(A,B,C,……)
    if(!pressed_keys.includes(keyName) && scale.length>0){
        if(keys1.indexOf(keyName)>-1){
            MidiNoteOn(72+12*Math.floor(keys1.indexOf(keyName)/scale.length)+scale[keys1.indexOf(keyName)%scale.length],100);
        }else if(keys2.indexOf(keyName)>-1){
            MidiNoteOn(60+12*Math.floor(keys2.indexOf(keyName)/scale.length)+scale[keys2.indexOf(keyName)%scale.length],100);
        }else if(keys3.indexOf(keyName)>-1){
            MidiNoteOn(48+12*Math.floor(keys3.indexOf(keyName)/scale.length)+scale[keys3.indexOf(keyName)%scale.length],100);
        }
        pressed_keys.push(keyName);
    }
});
document.addEventListener('keyup', (event) => {
    var keyName = event.key;
    console.log(keyName+" released");
    //文字キーが押されたときの反応(A,B,C,……)
    if(scale.length>0){
        if(keys1.indexOf(keyName)>-1){
            MidiNoteOff(72+12*Math.floor(keys1.indexOf(keyName)/scale.length)+scale[keys1.indexOf(keyName)%scale.length]);
        }else if(keys2.indexOf(keyName)>-1){
            MidiNoteOff(60+12*Math.floor(keys2.indexOf(keyName)/scale.length)+scale[keys2.indexOf(keyName)%scale.length]);
        }else if(keys3.indexOf(keyName)>-1){
            MidiNoteOff(48+12*Math.floor(keys3.indexOf(keyName)/scale.length)+scale[keys3.indexOf(keyName)%scale.length]);
        }
        pressed_keys.splice(pressed_keys.indexOf(keyName),1);
    }
});

function indicateScaleKeys() {
    console.log("indicate scale keys");
    console.log(scale);
    for(let i=0; i<128; i++){
        if(scale.includes(i%12)){
            $("#"+i.toString()).addClass("scale");
        }else{
            $("#"+i.toString()).removeClass("scale");
        }
    }
}

mousePressedKeys=[];
function keyMousePressed(e){
    noteNum = e.data.note;
    MidiNoteOn(noteNum,100);
    mousePressedKeys.push(noteNum);
}
function keyMouseReleased(){
    mousePressedKeys.forEach(e => {
        MidiNoteOff(e);
    });
    mousePressedKeys=[];
}

var keynames = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"];
var blackkeys = [1,3,6,8,10];
var scale = [0, 2, 3, 5, 7, 8, 10]
$(function(){
    //GUでのピアノキーの生成
    for(let i = 0; i<128; i++){
        //白黒の色を分ける
        if(blackkeys.includes(i%12)){
            $("#piano").append("<div class='piano_key_black' id='"+i.toString()+"'>"+keynames[i%12]+Math.floor(-2+i/12).toString()+"</div>");
        }else{
            $("#piano").append("<div class='piano_key' id='"+i.toString()+"'>"+keynames[i%12]+Math.floor(-2+i/12).toString()+"</div>");
        }
        //キーがマウスで押されたときの処理
        $("#"+i.toString()).on("mousedown",{note: i},keyMousePressed);
        //キーが離されたときの処理
        $("#"+i.toString()).on("mouseup",keyMouseReleased);
    }
    indicateScaleKeys();
});
