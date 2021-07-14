var addedTags = [];

$(document).ready(
    // animation for forms start
    function () {
        $(".vr-div").css({
            height: $("#reg-form").height()
        });
        $("#or-span").css({
            top: ($("#reg-form").height() / 2),
            right: ($("#or-span").width() / 2)
        });
        $(".animeted-form .form-control").focus(
            function () {
                $(this).prev().css({ "z-index": 2 });
                $(this).prev().toggleClass("lbl-color-set");
                $(this).prev().animate({ top: "0px", left: 0, "font-size": "12px" }, 290);
            }
        );
        $(".animeted-form .form-control").blur(
            function () {
                if (!$(this).val()) {

                    $(this).prev().css({ "z-index": 0 });
                    $(this).prev().toggleClass("lbl-color-set");
                    $(this).prev().animate({ top: "28px", left: "8px", "font-size": "16px" }, 290);
                }
            }
        );
        // animation for forms end


        // categores column animation start

        $(".categores-list").mouseleave(function () {
            $(".cateogry-act-border").animate({ height: "40px" });

        });
        $(".cateogry-item").hover(function () {
            // over
            if (!$(this).hasClass("cateogry-active")) {
                $(".cateogry-act-border").animate({ height: 0 });
                $(this).nextAll(".cateogry-border").css("width", "3px")
                $(this).nextAll(".cateogry-border").animate({ height: "40px" });

            }
        }, function () {
            // out
            if (!$(this).hasClass("cateogry-active")) {
                $(this).nextAll(".cateogry-border").css("width", "0px")
                $(this).nextAll(".cateogry-border").animate({ height: "0px" });
            }
        }
        );
        $(".cateogry-active").mouseenter(function () {
            $(".cateogry-act-border").animate({ height: "40px" });

        });

        $(".subcategories-list").slideUp(0);
        $(".category-li .down-icon").click(function (e) { 
            if( !$(this).hasClass("down-icon-a")){
            $(this).css("animation-name","none");
            $(this).css("animation-name","down-icon-ani");
        
        }else{
            $(this).css("animation-name","none");
            // $(this).css("animation-direction","reverse");
            $(this).css("animation-name","down-icon-ani2");
            
        }
            $(this).toggleClass("down-icon-a");
            $(this).nextAll(".subcategories-list").slideToggle();
        });

        startGridQueAni("grid-questions", 100);//gird question animetion
        startGridQueAni("tags-reg", 50);//gird question animetion
        startGridQueAni("grid-tags", 50);//gird question animetion
        // custom select 
        $(".btn-select").click(function (e) {
            e.preventDefault();
            $(".custom-select-list").css({
                visibility: "hidden"

            });
            $(this).next().css({
                visibility: "visible"

            });
            if (!$(this).hasClass("btn-select-act"))
                $(this).toggleClass("btn-select-act");
        }
        );
        $(window).click(function () {
            const lists = document.querySelectorAll(".custom-select-list");
            for (var i = 0; i < lists.length; i++) {
                if ($(lists[i]).css("visibility") === "visible") {
                    $(lists[i]).css({
                        visibility: "hidden"

                    });
                    $(lists[i]).prev().toggleClass("btn-select-act");

                }
            }
            $(".tags-list").css({ display: "none" });

        });
        $(".custom-select").click(function (event) {
            event.stopPropagation();
        });
        $(".tags-list").click(function (event) {
            event.stopPropagation();
        });
        $(".custom-select-item").click(function () {
            $(this).parent().prev().text("");
            $(this).parent().prev().append("<span class=\"selected-span\">" + $(this).text() + "</span>");
            $(this).parent().prev().append("<i class=\"fas fa-caret-down select-arrow\"></i>")
            $(this).parent().css({
                visibility: "hidden"

            });
            $(this).parent().prev().toggleClass("btn-select-act");
        }
        );
        // custom select end
        //editor start
        if (document.getElementById("editor") != undefined) {
            var tinyMDE = new TinyMDE.Editor({ element: 'editor', content: " " });
            var commandBar = new TinyMDE.CommandBar({ element: 'editor-toolbar', editor: tinyMDE });
        }

        // tag list start
        $("#que-tags-input").keydown(function (e) {

            if (e.which == 38 || e.which == 40)
                e.preventDefault();
            else if (e.which == 13) {
                var tagText = $(".current-list-tag").text();
                $(this).val("");
                $(".current-list-tag").removeClass("current-list-tag");
                if (tagText)
                    addTagBtn(tagText,$(this).data("tags-div"));

            }

        })
        var currentPos = 0;
        $("#que-tags-input").keyup(function (e) {
            if (!(e.which == 40 || e.which == 38))
                currentPos = 0;

            if ($(this).text().length == 1)
                $(".current-list-tag").removeClass("current-list-tag");

            var found = 0;
            var hasHover = null;
            $(this).next().children().map(function (c) {
                if (!$(this).text().startsWith($("#que-tags-input").val()) || addedTags.includes($(this).text()))
                    $(this).hide()
                else {
                    found++;
                    $(this).show();
                }
                if ($(this).hasClass("current-list-tag"))
                    hasHover = this;
            });
            if ($(this).val() == "" || found == 0)
                $(this).next().css({ display: "none" });
            else
                $(this).next().css({ display: "block" });
            if (e.which == 38) {
                if (hasHover == null) {
                    $(this).next().children().last().addClass("current-list-tag");
                }
                else {
                    $(hasHover).removeClass("current-list-tag");
                    $(hasHover).prevAll("li:visible").first().addClass("current-list-tag");
                    currentPos--;

                }
                console.log(currentPos);

                if (currentPos <= 0) {
                    currentPos = found;

                    $(this).next().animate({
                        scrollTop: $(this).next().prop("scrollHeight")
                    }, 200);
                    $(".current-list-tag").removeClass("current-list-tag");
                    $(hasHover).removeClass("current-list-tag");
                    $(this).next().children().last().addClass("current-list-tag");

                }
                else if (currentPos <= found - 3)
                    $(this).next().animate({
                        scrollTop: "-=" + ($(".tags-list-item").height() + 2)
                    }, 200);

            }
            else if (e.which == 40) {
                if (hasHover == null) {
                    currentPos = 1;
                    $(this).next().children().first("li:visible").addClass("current-list-tag");
                }
                else {

                    $(hasHover).removeClass("current-list-tag");
                    $(hasHover).nextAll("li:visible").first().addClass("current-list-tag");
                    currentPos++;
                }


                if (currentPos > found) {
                    currentPos = 1;

                    $(this).next().animate({
                        scrollTop: '0'
                    }, 200);
                    $(hasHover).removeClass("current-list-tag");
                    $(this).next().children().first().addClass("current-list-tag");

                }

                if (currentPos >= 3)
                    $(this).next().animate({
                        scrollTop: '+=' + ($(".tags-list-item").height() + 2)
                    }, 200);

            }

        });
        $(".tags-list-item").click(function () {

            var tagText = $(this).text();

            addTagBtn(tagText);
            $(this).parent().css({ display: 'none' });
        });
        // tag list end

        // form validtion start
        // register
        var oldPass = ""
        var oldPassC = ""
        var oldEmail = ""
        $("#password-input").keyup(function (e) {
            if (oldPass != $(this).val()) {
                $(this).next().slideUp();
                $("#confirmPassword-input").next().slideUp();
            }
            oldPass = $(this).val();
        });
        $("#confirmPassword-input").keyup(function (e) {
            if (oldPassC != $(this).val())
                $(this).next().slideUp();
            oldPassC = $(this).val();
        });
        $("#email-input").keyup(function (e) {
            if (oldEmail != $(this).val())
                $(this).next().slideUp();
            oldEmail = $(this).val();
        });
        $(".error-p").slideUp(0);
        $("#reg-btn").click(function (e) {
            var isEmpyty = false;
            const emailPatt = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/gm;
            $("#reg-form .form-input").map(function () {
                if (!$(this).val() && !$(this).next().hasClass("r-error-span")) {
                    $(this).next().find(".error-val").text("This Field is required");
                    $(this).next().slideDown();
                    isEmpyty = true;
                    $(this).focus(function () {
                        $(this).next().slideUp();

                    });
                }

            });
            if (isEmpyty) {
                e.preventDefault();
            } else if (!emailPatt.test($("#email-input").val())) {
                $("#email-input").next().find(".error-val").text("Email not valid");
                $("#email-input").next().slideDown();
                e.preventDefault();

            }
            else if ($("#password-input").val().length < 8) {
                $("#password-input").next().find(".error-val").text("Password should be 8 charters or more");
                $("#password-input").next().slideDown();
                e.preventDefault();

            }
            else if ($("#password-input").val() != $("#confirmPassword-input").val()) {
                $("#confirmPassword-input").next().find(".error-val").text("Password does not match");
                $("#confirmPassword-input").next().slideDown();
                e.preventDefault();

            }
        })
        // form validtion end

        // tabs start
        // buttons tab
        $('.tab-btn').click(function () {


            $(".act-tab").css({
                "animation-name": "tab-ani",
                "animation-duration": ".2s",
                "animation-fill-mode": "forwards",
                "animation-direction": "reverse"

            });
            ;
            let clicked = this;

            const tr = setTimeout(function () {
                $(".act-tab").css({
                    "animation-name": "none",
                    "animation-duration": "0s",
                    "animation-fill-mode": "backwards",
                    "animation-direction": "normal"

                });
                $(clicked).siblings().removeClass("act-tab");
            }, 200);

            $(this).css({
                "animation-name": "tab-ani",
                "animation-duration": ".2s",
                "animation-fill-mode": "forwards",
                "animation-direction": "normal"

            });

            const ta = setTimeout(function () {
                $(clicked).addClass("act-tab");
                $(clicked).css({
                    "animation-name": "none",
                    "animation-duration": "0s",
                    "animation-fill-mode": "backwards",
                    "animation-direction": "normal",
                });
            }, 200);
            $($(this).data("content-parent") + "> .content-tab").css("display", "none");
            let conId = $(this).data("content");
            $(conId).css("display", "block");

        });
        // flat tabs
        $(".tab-flat").click(function () {
                $(this).siblings().removeClass("act-tab");
                $(this).addClass("act-tab");
                $($(this).data("content-parent") + " > .content-tab").css("display", "none");
                $($(this).data("content")).css("display","block");
                console.log($(this).data("content"));
            }
        );
        //tabs button simple
        $('.tab-btn-sim').click(function () {

            $(this).siblings().removeClass("act-tab-sim");
            $(this).addClass("act-tab-sim");
            $($(this).data("content-parent") + "> .content-tab").css("display", "none");
            let conId = $(this).data("content");
            $(conId).css("display", "block");

        });
        // tabs end
        $(".num-tag").hover(
            function () {
                // over
                $(this).find(".num-in-tb").css("border-right","1px solid #fff");
            }, function () {
                // out
                $(this).find(".num-in-tb").css("border-right","inherit");

            }
        );
            // side list start
            $(".side-list-item").click(function(){
                $(this).siblings().removeClass("side-list-item-act");
                $(this).addClass("side-list-item-act");
                $($(this).data("content-p")+" .side-list-content").css("display", "none");
                $($(this).data("content-p")+" "+$(this).data("content")).css("display", "block");
            })
            // side list end

            $(".remove-tag-btn").click(function (e) { 
                console.log("test");
                $(this).parent().addClass("remove-grid-item");
                let clicked=this;
                function aniCallBack(){
                $(clicked).parent().css("display","none");
                    
                }
                let aniTimeOut=setTimeout(aniCallBack,185);
            });
            $(".add-comment-span").click(function(){
                if($(this).nextAll(".add-comment-div").css("display")=="none")
                    $(this).nextAll(".add-comment-div").css("display","block")
                else
                    $(this).nextAll(".add-comment-div").css("display","none")
            });
        }

);
//gird question animetion funcrion
function startGridQueAni(parentId, duriton = 100) {
    var iQue = 0;
    function sacleQueGrid() {
        try {
            $(document.getElementById(parentId).childNodes[iQue]).addClass("item-grid-ani-" + duriton);

            iQue++;
            if (document.getElementById(parentId).childNodes.length < iQue)
                clearInterval(interVal)
        } catch (e) {
            clearInterval(interVal);
        }
    }
    var interVal = setInterval(sacleQueGrid, 100);
}
function addTagBtn(tagText,tagsDivId) {
    let buttonTag = document.createElement("button");
    $(buttonTag).addClass(["btn", "btn-outline-info", "btn-tag", "item-grid-ani-100","btn-tag-removeable"]);
    $(buttonTag).attr("type", "button");
    $(buttonTag).text(tagText);
    let removeBtn=document.createElement("div");
    $(removeBtn).addClass(["btn" ,"remove-tag-btn"]);
    $(removeBtn).append("<i class=\"fas fa-times\"></i>");
    $(buttonTag).append(removeBtn);
    $(tagsDivId).append(buttonTag);

    $(removeBtn).click(function (e) { 
        $(this).parent().addClass("remove-grid-item");
        let clicked=this;
        function aniCallBack(){
        $(clicked).parent().css("display","none");
            
        }
        let aniTimeOut=setTimeout(aniCallBack,185);
    });
    addedTags.push(tagText);
}