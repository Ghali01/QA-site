$(document).ready(
    function(){
        $(".vr-div").css({
            height: $("#reg-form").height()
        });
        $("#or-span").css({
            top:($("#reg-form").height()/2),
            right:($("#or-span").width()/2)
        });
        console.log($("#or-span").width());
        $(".form-control").focus(
            function(){
                $(this).prev().css({"z-index":2,color: "rgba(219, 99, 29, 0.925)"});
                $(this).prev().animate({top:"0px",left:0,"font-size":"12px"},290);
            
        }
        );
        $(".form-control").blur(
            function(){
                if(!$(this).val()){
            
                $(this).prev().css({"z-index":0,color: "gray"});
                $(this).prev().animate({top:"28px",left:"8px","font-size":"16px"},290);
                }
            }
        );
    }
);