jQuery = $ = require('jquery');
var keynames = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
var blackkeys = [1,3,6,8,10]
$(function(){
    //GUでのピアノキーの生成
    for(let i = 0; i<128; i++){
        if(blackkeys.includes(i%12)){
            $("#piano").append("<div class='piano_key_black' id='piano_key"+i.toString()+"'>"+keynames[i%12]+Math.floor(-2+i/12).toString()+"</div>");
        }else{
            $("#piano").append("<div class='piano_key' id='piano_key"+i.toString()+"'>"+keynames[i%12]+Math.floor(-2+i/12).toString()+"</div>");
        }
    }

    
});
