$(document).ready(
// animation for forms start
    function(){
        $(".vr-div").css({
            height: $("#reg-form").height()
        });
        $("#or-span").css({
            top:($("#reg-form").height()/2),
            right:($("#or-span").width()/2)
        });
        $(".animeted-form .form-control").focus(
            function(){
                $(this).prev().css({"z-index":2});
                $(this).prev().toggleClass("lbl-color-set");
                $(this).prev().animate({top:"0px",left:0,"font-size":"12px"},290);
        }
        );
        $(".animeted-form .form-control").blur(
            function(){
                if(!$(this).val()){
            
                $(this).prev().css({"z-index":0});
                $(this).prev().toggleClass("lbl-color-set");
                $(this).prev().animate({top:"28px",left:"8px","font-size":"16px"},290);
                }
            }
        );
        // animation for forms end

    
        // categores column animation start
    
        $(".categores-list").mouseleave(function () { 
            $(".cateogry-act-border").animate({height:"40px"}); 

        });
        $(".cateogry-item").hover(function () {
            // over
            if(!$(this).hasClass("cateogry-active")){
                    $(".cateogry-act-border").animate({height:0}); 
                $(this).next().css("width","3px")
                $(this).next().animate({height:"40px"}); 
            
            }
            }, function () {
            // out
            if(!$(this).hasClass("cateogry-active")){
                $(this).next().css("width","0px")
                $(this).next().animate({height:"0px"}); 
            }
        }
    );
        $(".cateogry-active").mouseenter(function () { 
            $(".cateogry-act-border").animate({height:"40px"}); 
            
        });

        // categores column animation end


        $(document).scroll(function () { 
            if($(document).scrollTop()!=0)
                $(".left-column, .right-column").css("top","30px")
            else
                $(".left-column, .right-column").css("top","70px")

            });

            startGridQueAni("grid-questions",100);//gird question animetion
            startGridQueAni("tags-reg",50);//gird question animetion
            
        }

);
//gird question animetion funcrion
function startGridQueAni(parentId,duriton=100){
    var iQue=0;
    function sacleQueGrid(){
    try{    
    $( document.getElementById(parentId).childNodes[iQue]).addClass("item-grid-ani-"+duriton);
   
    iQue++;
    if(document.getElementById(parentId).childNodes.length<iQue)
        clearInterval(interVal)
    }catch(e){
        clearInterval(interVal);
    }
    }
    var interVal=setInterval(sacleQueGrid, 100);
}