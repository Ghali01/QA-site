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
        console.log($("#or-span").width());
        $(".animeted-form .form-control").focus(
            function(){
                $(this).prev().css({"z-index":2,color: "rgba(219, 99, 29, 0.925)"});
                $(this).prev().animate({top:"0px",left:0,"font-size":"12px"},290);
            
        }
        );
        $(".animeted-form .form-control").blur(
            function(){
                if(!$(this).val()){
            
                $(this).prev().css({"z-index":0,color: "gray"});
                $(this).prev().animate({top:"28px",left:"8px","font-size":"16px"},290);
                }
            }
        );
        // animation for forms end
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

}

);