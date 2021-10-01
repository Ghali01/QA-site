$(document).ready(function(){
    $('.crop-img').mousedown(cropMouseDown);
    $('.crop-img').mousemove(move);
    $('.crop-img').mouseup(cropMouseUp);
    $('body').mouseup(_=>
        {
           try {
                $('.crop-img').trigger('mouseup');
            }
            catch(e){}
        });
    $('.b-hand').mousedown(resize);
    $('.l-hand').mousedown(resize);
    $('.t-hand').mousedown(resize);
    $('.r-hand').mousedown(resize);
    $('.edit-avatar-btn').click(editAvatrClick);
    $('.save-avt-form').click(saveAvtBtn);
});
var scx,scy,startCropx0,startCropx1,startCropy0,startCropy1;
var moveing=false;

var startMoveH,startMoveW,startMoveL,startMoveT;
function move(e){
    e.preventDefault(); 
    if(moveing ) {
        let dy=e.pageY-scy
        let dx=e.pageX-scx
        console.log(dx,dy);
        let newT=startMoveT+(dy);
        let newL=startMoveL+(dx);
        console.log(newL,newT);
        if(newT>0 && newT<$('.crop-img').parent().height()-startMoveH)
          $('.crop-img').css('top',(newT)+'px');
        if(newL>0 && newL<$('.crop-img').parent().width()-startMoveW)
          $('.crop-img').css('left',(newL)+'px');
        }
   
    
}

    function cropMouseDown(e){
    // $('.crop-img').parent().mousemove(move);
    scx=e.pageX;
    scy=e.pageY;
    // if(!startCropy1)
    startMoveH=$(this).height();
    startMoveW=$(this).width();
    startMoveL=$(this).position().left;
    startMoveT=$(this).position().top;
    startCropx1=$(this).parent().width()-($(this).position().left+$(this).width());
        console.log(scy);
    startCropy1=$(this).parent().height()-($(this).position().top+$(this).height());
    moveing=true;
}
function cropMouseUp(){
    moveing=false;


}
function getXYT(el2){
    let el= $('.crop-img');
    let mtrx=$('.crop-img').css('transform').slice(7,-1).split(',');
    console.log(mtrx);
    return {
        x:mtrx[4],
        y:mtrx[5]
    }
}


function resize(e){
    $('.crop-img').off('mousemove');
    let s,dalta,oldSize,newSize,moveDalta,xy,mvTarget;
    startMoveL=$('.crop-img').position().left;
    startMoveT=$('.crop-img').position().top;
    if ($(this).hasClass('b-hand')||$(this).hasClass('t-hand')){
        s=e.pageY;
        oldSize=$('.crop-img').height();
    }
    if ($(this).hasClass('l-hand')||$(this).hasClass('r-hand')){
        s=e.pageX;
        oldSize=$('.crop-img').width();
    }
    let f1 =e=>{
        if ($(this).hasClass('b-hand'))
            dalta=e.pageY-s;
        if ($(this).hasClass('t-hand')){
            dalta=-1*(e.pageY-s);
            mvTarget='top';
            moveDalta=(startMoveT+(-1*dalta));
       
        
        }

        if ($(this).hasClass('l-hand')){
                dalta=-1*(e.pageX-s);
                mvTarget='left';
                moveDalta=(startMoveL+(-1*dalta));
            }
        if ($(this).hasClass('r-hand'))
            dalta=e.pageX-s;
        
        newSize=oldSize+(dalta);
        let cssObj = {
            'height':newSize+'px',
            'width':newSize+'px',
            [mvTarget]:moveDalta+'px'
        } 
        if($('.crop-img').position().top+$('.crop-img').height()+2>=$('.crop-img').parent().height()){
        moveDalta=(startMoveT+(-1*dalta));
        cssObj['top']=moveDalta+'px';
        }
       if($('.crop-img').position().left+$('.crop-img').width()+2>=$('.crop-img').parent().width()){
        mvTarget='left';
        moveDalta=(startMoveL+(-1*dalta));
        cssObj['left']=moveDalta+'px';
    
        }
        if($(this).hasClass('t-hand')&&$('.crop-img').position().top<=3&&dalta>0){
            cssObj['top']=($('.crop-img').height().dalta)+'px';
        }
        if($(this).hasClass('l-hand')&&$('.crop-img').position().left<=3&&dalta>0){
            cssObj['left']=($('.crop-img').width().dalta)+'px';
        }

        if(newSize>150&&newSize<360 ) 
            $('.crop-img').css(cssObj);
    
    };
    $(this).mousemove(f1);
    $('.crop-img').mousemove(f1);
    $('.avatar-container').mousemove(f1);
    $(document).mousemove(f1);
    
        
    let f2=_=>{ 
        $(this).off('mousemove');
        $('.avatar-container').off('mousemove');
        $(document).off('mousemove');    
        $('.crop-img').off('mousemove');    
        $('.crop-img').off('mouseup');    
        $('.crop-img').off('mousedown');    
        $('.crop-img').mouseup(cropMouseUp);
        $('.crop-img').mousedown(cropMouseDown);
        $('.crop-img').mousemove(move);
    }
    $(this).mouseup(f2); 
    $('.avatar-container').mouseup(f2); 
    $('.crop-img').mouseup(f2); 

}

function editAvatrClick(){
    $('#avt-file').click();   
    $('#avt-file').change(function (e) { 
        const file= this.files[0];
        if(file){
            const reder=new FileReader()
            reder.addEventListener('load',function(){
                $('.e-avatar-img').attr('src',this.result);
                const model = new bootstrap.Modal(document.querySelector('#avatarModal'));
                model.show();
            
            })
            reder.readAsDataURL(file);
        }
    });
}

function saveAvtBtn(){

    const obj={
        x:$('.crop-img').position().left,
        y:$('.crop-img').position().top,
        height:$('.crop-img').height(),
        width:$('.crop-img').width(),
        orginalW:$('.e-avatar-img').width(),
        orginalH:$('.e-avatar-img').height(),
    }
    $('#postion').val(JSON.stringify(obj));
    $('#change-avt-form').submit();
}