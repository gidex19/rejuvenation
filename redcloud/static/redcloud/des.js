
var tag_btn = document.querySelectorAll('#tag_btns');
//console.log(tag_btn);
//tag_btn.addEventListener('click',function(){
//    console.log('tag button clicked');
//})
for(tag of tag_btn){
    //console.log(tag);
    tag.addEventListener('mouseover' , function(e){
        e.target.className = "btn btn-md btn-info mt-1 mb-1";
        //console.log(e.target.className);   
    })
    tag.addEventListener('mouseout' , function(e){
        e.target.className = "btn btn-sm btn-info mt-1 mb-1";
        //console.log(e.target.className);   
    })
} 