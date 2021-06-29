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
            startGridQueAni("grid-tags",50);//gird question animetion
            // custom select 
            $(".btn-select").click(function(e){
                e.preventDefault();
                $(".custom-select-list").css({
                visibility:"hidden"

                });
                $(this).next().css({
                visibility:"visible"

                });
                if(!$(this).hasClass("btn-select-act"))
                    $(this).toggleClass("btn-select-act");
            }
            );
            $(window).click(function() {
               const lists= document.querySelectorAll(".custom-select-list");
               for(var i=0 ;i<lists.length;i++){
                    if($(lists[i]).css("visibility")==="visible"){
                        $(lists[i]).css({
                            visibility:"hidden"
            
                            });
                    $(lists[i]).prev().toggleClass("btn-select-act");
                            
                    }
                }
            });
            $(".custom-select").click(function(event){
            event.stopPropagation();
            });
            $(".custom-select-item").click( function(){
                $(this).parent().prev().text("");
                $(this).parent().prev().append("<span class=\"selected-span\">"+ $(this).text()+"</span>");
                $(this).parent().prev().append("<i class=\"fas fa-caret-down select-arrow\"></i>")
                $(this).parent().css({
                    visibility:"hidden"
    
                    });
                $(this).parent().prev().toggleClass("btn-select-act");
                }
            );
            // custom select end
            //editor start
            if(document.getElementById("editor")!=undefined){
            var tinyMDE = new TinyMDE.Editor({element: 'editor',content:" "});
            var commandBar = new TinyMDE.CommandBar({element: 'editor-toolbar', editor: tinyMDE});
            }
            $("#que-tags-input").keydown(function (e) {

                if(e.which==38||e.which==40)
                    e.preventDefault();
             })
             var currentPos=0;
            $("#que-tags-input").keyup(function (e) { 

                if($(this).text().length==1)
                    $(".current-list-tag").removeClass("current-list-tag");
                
                var  found=0;
                var hasHover=null;
                $(this).next().children().map(function(c){
                    if(!$(this).text().startsWith($("#que-tags-input").val()))
                        $(this).hide()
                    else{
                        found++;
                        $(this).show();
                    }
                    if($(this).hasClass("current-list-tag"))
                        hasHover=this;
                });
                if($(this).val()==""|| found==0)
                $(this).next().css({display:"none"});
                else
                    $(this).next().css({display:"block"});
                // console.log(e.which);
                if(e.which==38){
                    if(hasHover==null)
                    $(this).next().children().last().addClass("current-list-tag");
                else{
                    $(hasHover).removeClass("current-list-tag");
                    $(hasHover).prevAll("li:visible").first().addClass("current-list-tag");
                currentPos--;
                }
                
                                   
                $(this).next().animate({
                    scrollTop: "-=26"
                  }, 200);
            
                }
                else if(e.which==40){
                    if(hasHover==null){
                        $(this).next().children().first("li:visible").addClass("current-list-tag");
                    }                    
                    else{

                        
                        $(hasHover).removeClass("current-list-tag");
                        $(hasHover).nextAll("li:visible").first().addClass("current-list-tag");
    
                    }
                    currentPos++;
                    console.log(currentPos);
                    if(currentPos>found){
                        currentPos=0;
                                           
                        $(this).next().animate({
                            scrollTop: '0'
                        }, 200);
                        $(hasHover).removeClass("current-list-tag");
                        $(this).next().children().first().addClass("current-list-tag");
    
                    }
                    if(currentPos>=3)                    
                        $(this).next().animate({
                            scrollTop: '+=30'
                        }, 200);
                        }
                    
            });
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