jQuery = $ = require('jquery');
var keynames = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"];
var blackkeys = [1,3,6,8,10];
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
        $("#"+i.toString()).on("mousedown",function(){
            console.log(i.toString()+" pressed");
        });
        //キーが離されたときの処理
        $("#"+i.toString()).on("mouseup",function(){
            console.log(i.toString()+" released");
        });
    }

    
});
