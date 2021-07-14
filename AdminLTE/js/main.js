var addedTags = [];

$(document).ready(function () {
    // todo
    try{

    $('#summernote').summernote();
    }catch(e){}
    $(".category-list-item").click(CategoryListClick);
    $(".categories-list").children().first().click();

    $(".add-cate-m-btn").click(addCateClick);
    $(".del-tag-btn").click(deleteTagBtn);
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
                console.log(e.which);
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
    
            $(".btn-tag-removeable").hover(function () {
                // over
                $(this).find(".remove-tag-btn").css("border-color", "white");    
            }, function () {
                // out
                $(this).find(".remove-tag-btn").css("border-color", "var(--third-color)");    

            }
        );
        $(".remove-tag-btn").click(function (e) { 
            console.log("test");
            $(this).parent().addClass("remove-grid-item");
            let clicked=this;
            function aniCallBack(){
            $(clicked).parent().css("display","none");
                
            }
            let aniTimeOut=setTimeout(aniCallBack,185);
        });    
        $(".del-cate-btn").click(deleteCateBtn);
        $(".ban-user-btn").click(banUserBtn);
    }
);
function CategoryListClick(e) { 
    if(!$(this).hasClass("active")){
    $(this).addClass("active");
    $(this).siblings().removeClass("active");
    let subs=$(this).data("sub");
    let nextList=$(this).closest(".list-col").next(".list-col").find(".categories-list");
    $(this).closest(".list-col").nextAll(".list-col").map(function(){ 
        $(this).find(".categories-list").text('');
    }
    );
    if(subs)    
    subs.forEach(element => {
        let cateLi=document.createElement('li');
        $(cateLi).addClass(["list-group-item" ,"category-list-item"]);
        $(cateLi).attr("data-sub", JSON.stringify(element['sub']));
        $(cateLi).attr("data-cate-id", element['id']);
        let spanName=document.createElement("span");
        $(spanName).text(element['name']);
        $(spanName).addClass("category-name");
        $(cateLi).append(spanName);
        let deleteBtn=document.createElement("button");
        $(deleteBtn).addClass(["btn ","btn-app" , "cus-btn-app" ,"btn-app-sm ","float-right" ,"del-cate-btn"]);
    //  data-lvl="2" data-toggle="modal" data-target="#add-cate-modal"

        $(deleteBtn).attr("data-lvl","2");
        $(deleteBtn).attr("data-toggle","modal");
        $(deleteBtn).attr("data-target","#del-cate-modal");
        $(deleteBtn).append('<i class="far fa-trash-alt btn-app-icon"></i>Delete');
        $(deleteBtn).click(deleteCateBtn);        
        $(cateLi).append(deleteBtn);
        $(cateLi).click(CategoryListClick);
        $(nextList).append(cateLi);            
    });
    $(nextList).children().first().click();}
}

// var listToAddId;
function addCateClick (e) { 
    let prevLiActId=$(this).closest(".list-col").prev(".list-col").find(".categories-list").find(".active").data("cate-id");
    let lvl=$(this).data("lvl");
    if (lvl =='1'){
        prevLiActId='-1';
    }
    $("#add-cate-id").val(prevLiActId);
    $("#add-cate-lvl").val(lvl)   
    

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
    $(buttonTag).hover(function () {
        // over
        $(this).find(".remove-tag-btn").css("border-color", "white");    
    }, function () {
        // out
        $(this).find(".remove-tag-btn").css("border-color", "var(--third-color)");    

    }
);
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
function deleteCateBtn(){
    $("#del-cate-id").val($(this).parent().data("cate-id"));
    $("#del-cate-name").text($(this).prevAll(".category-name").text());
}
function deleteTagBtn(){
    $("#del-tag-id").val($(this).data("tag-id"));
    $("#del-tag-name").text($(this).data("tag-name"));
}
function banUserBtn(){
    $("#ban-user-name").text($(this).data("user-name"));
    $("#ban-user-id").val($(this).data("user-id"));
}