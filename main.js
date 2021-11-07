const { forEach } = require('lodash');

var midi = null;
var midiout = null;
var input_devices = [];
var output_devices = [];

//jquery読み込み
jQuery = $ = require('jquery');
//web midi使用
navigator.requestMIDIAccess().then(onMIDISuccess,onMIDIFailure);
function onMIDIFailure(msg){
    console.log("onMIDIFailure(): "+msg);
    window.alert("[エラー]MIDIへのアクセスに失敗しました。");
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

pressed_midi_keys = [];
//MIDIノート信号送信
function MidiNoteOn(note, vel){
    if(midiout != null && !pressed_keys.includes(note)){
        console.log("note on")
        midiout.send([0x90,note,vel]);
        if($("#"+note.toString()).attr("class")=="piano_key"){
            $("#"+note.toString()).css("background-color","gray");
        }else{
            $("#"+note.toString()).css("background-color","dimgray");
        }
        pressed_midi_keys.push(note);
    }
}
//MIDIノートオフ信号送信
function MidiNoteOff(note){
    if(midiout != null && pressed_midi_keys.includes(note)){
        console.log("note off")
        midiout.send([0x90,note,0x00]);
        $("#"+note.toString()).css("background-color","");
        pressed_midi_keys.splice(pressed_midi_keys.indexOf(note),1);
    }
}


var keys1 = ["q","w","e","r","t","y","u","i","o","P","@","["];
var keys2 = ["a","s","d","f","g","h","j","k","l",";",":","]"];
var keys3 = ["z","x","c","v","b","n","m",",",".","/","_"];
var chordkeys = ["1","2","3","4","5","6","7"];
pressed_keys=[]
//文字のキー入力
document.addEventListener('keydown', (event) => {
    var keyName = event.key;
    console.log(keyName+" pressed");
    //文字キーが押されたときの反応(A,B,C,……)
    if(!pressed_keys.includes(keyName) && scale.length>0){
        if(keys1.indexOf(keyName)>-1){
            MidiNoteOn(baseNote+12+12*Math.floor(keys1.indexOf(keyName)/scale.length)+scale[keys1.indexOf(keyName)%scale.length],velocity);
        }else if(keys2.indexOf(keyName)>-1){
            MidiNoteOn(baseNote+12*Math.floor(keys2.indexOf(keyName)/scale.length)+scale[keys2.indexOf(keyName)%scale.length],velocity);
        }else if(keys3.indexOf(keyName)>-1){
            MidiNoteOn(baseNote-12+12*Math.floor(keys3.indexOf(keyName)/scale.length)+scale[keys3.indexOf(keyName)%scale.length],velocity);
        }else if(chordkeys.includes(keyName)){
            MidiNoteOn(baseNote+12*Math.floor((parseInt(keyName)-1)/scale.length)+scale[(parseInt(keyName)-1)%scale.length],velocity);
            MidiNoteOn(baseNote+12*Math.floor((parseInt(keyName)+1)/scale.length)+scale[(parseInt(keyName)+1)%scale.length],velocity);
            MidiNoteOn(baseNote+12*Math.floor((parseInt(keyName)+3)/scale.length)+scale[(parseInt(keyName)+3)%scale.length],velocity);
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
            MidiNoteOff(baseNote+12+12*Math.floor(keys1.indexOf(keyName)/scale.length)+scale[keys1.indexOf(keyName)%scale.length]);
        }else if(keys2.indexOf(keyName)>-1){
            MidiNoteOff(baseNote+12*Math.floor(keys2.indexOf(keyName)/scale.length)+scale[keys2.indexOf(keyName)%scale.length]);
        }else if(keys3.indexOf(keyName)>-1){
            MidiNoteOff(baseNote-12+12*Math.floor(keys3.indexOf(keyName)/scale.length)+scale[keys3.indexOf(keyName)%scale.length]);
        }else if(chordkeys.includes(keyName)){
            MidiNoteOff(baseNote+12*Math.floor((parseInt(keyName)-1)/scale.length)+scale[(parseInt(keyName)-1)%scale.length]);
            MidiNoteOff(baseNote+12*Math.floor((parseInt(keyName)+1)/scale.length)+scale[(parseInt(keyName)+1)%scale.length]);
            MidiNoteOff(baseNote+12*Math.floor((parseInt(keyName)+3)/scale.length)+scale[(parseInt(keyName)+3)%scale.length]);
        }
        pressed_keys.splice(pressed_keys.indexOf(keyName),1);
    }
});

function allKeyRelease(){
    pressed_midi_keys.forEach(element => {
        MidiNoteOff(element);
    });
    pressed_midi_keys=[];
}

//スケールのキーを表示させる更新処理
function indicateScaleKeys() {
    console.log("indicate scale keys");
    console.log(scale);
    for(let i=0; i<128; i++){
        if(i == baseNote){
            $("#"+i.toString()).addClass("base");
        }
        else if($("#"+i.toString()).attr("class").split(' ').includes("base")){
                $("#"+i.toString()).removeClass("base");
        }
        if(scale.includes((i-baseNote%12+12)%12)){
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
    //スケールのカスタマイズ
    if(customize_mode){
        if(scale.includes((noteNum-baseNote+108)%12)){
            scale.splice(scale.indexOf((noteNum-baseNote+108)%12),1);
        }else{
            if(scale.length==0){
                scale.push((noteNum-baseNote+108)%12);
            }else{
                for(let i = 0; i<scale.length; i++){
                    if(scale[i]>(noteNum-baseNote+108)%12){
                        scale.splice(i,0,(noteNum-baseNote+108)%12);
                        break;
                    }
                }
                if(!scale.includes((noteNum-baseNote+108)%12)){
                    scale.push((noteNum-baseNote+108)%12);
                }
            }
        }
        indicateScaleKeys();
    }
}
function keyMouseReleased(){
    mousePressedKeys.forEach(e => {
        MidiNoteOff(e);
    });
    mousePressedKeys=[];
}

var keynames = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"];
var blackkeys = [1,3,6,8,10];
var scale = [0, 2, 4, 5, 7, 9, 11];
var scales = [
    {name: "Major", scale:[0, 2, 4, 5, 7, 9, 11]},
    {name: "Natural Minor", scale:[0, 2, 3, 5, 7, 8, 10]},
    {name: "All Notes", scale:[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]},
    {name: "Harmonic Minor", scale:[0, 2, 3, 5, 7, 8, 11]},
    {name: "Melodic Minor", scale:[0, 2, 3, 5, 7, 9, 11]},
    {name: "Major Penta Tonic", scale:[0, 2, 4, 7, 9]},
    {name: "Major Blues", scale:[0, 2, 3, 4, 7, 9]}
]
var baseNote = 60;
var velocity = 100;
var customize_mode = false;
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
        //キーがマウスのクリックから離されたときの処理
        $("#"+i.toString()).on("mouseup",keyMouseReleased);
    }
    //スクロール初期位置(C3らへん)
    $("#piano-wrapper").scrollLeft(1500);

    //基本音取得・表示変更
    function applyBaseNoteChange(){
        allKeyRelease();
        baseNote = parseInt($('[name=Base-Oct]').val())*12+24+keynames.indexOf($('[name=Base-Alpha]').val())
        indicateScaleKeys();
    }
    applyBaseNoteChange();
    $('[name=Base-Oct]').on("change",applyBaseNoteChange);
    $('[name=Base-Alpha]').on("change",applyBaseNoteChange);

    //ベロシティ変更
    $('[name=velocity]').on("input", function(){
        velocity = parseInt($("[name=velocity]").val());
        $("#velocity_indicator").text(velocity.toString());
    });

    //スケールリストの更新
    scales.forEach(element => {
        console.log(element);
        $("[name=scale]").append($('<option>').html(element.name).val(scales.indexOf(element).toString()));
    });
    $("[name=scale]").on("change",function () {
        allKeyRelease();
        scale = scales[parseInt($("[name=scale]").val())].scale.slice();
        indicateScaleKeys();
    });
    $("[name=customize]").on("change",function(){
        customize_mode = $("[name=customize]").prop("checked");
    })

    //midi出力リストの設定
    if(output_devices.length==0){
        console.log("waiting for applying output devices...");
        //MIDI出力の設定が正常にされるまで待つ
        timeout_i = 0;
        const intervalID = setInterval(function(){
            console.log(output_devices.length);
            if(output_devices.length == 0){
                if(i>6){
                    //タイムアウト
                    alert("[エラー]タイムアウトしました。利用可能なMIDI出力ポートがない可能性があります。");
                }else{
                    //ループ続行
                    i++
                    console.log("continue waiting...");
                    return;
                }
            }else{
                //outputリストの設定
                for(let i=0; i<output_devices.length; i++){
                    console.log(output_devices[i]);
                    $("[name=midiout]").append($('<option>').html(output_devices[i].name).val(output_devices.indexOf(output_devices[i]).toString()));
                }
                $("[name=midiout] option[value='0']").prop("selected",true);
                midiout = output_devices[0];
                $("[name=midiout]").on("change",function () {
                    allKeyRelease();
                    midiout = output_devices[parseInt($("[name=midiout]").val())];
                });
                clearInterval(intervalID);
            }
        },500);
    }
    
    //select要素のフォーカスを自動で解除
    const selects = document.querySelectorAll('select');
    for (const select of selects) {
        select.onfocus = (e) => e.target.blur();
    }
});