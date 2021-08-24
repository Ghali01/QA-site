var addedTags = [];

$(document).ready(function () {
    // todo
    try {

        $('#summernote').summernote();
    } catch (e) { }
    $('.category-select').change(onCategorySelectChange);
    $('.category-select').first().change();
    $(".category-list-item").click(CategoryListClick);
    $(".categories-list").children().first().click();
    $(".edit-cate-btn").click(editCateBtn);
    $(".add-cate-m-btn").click(addCateClick);
    $(".edit-tag-btn").click(editTagBtn);
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
            let tagText = $(".current-list-tag").text();
            let tagId = $(".current-list-tag").data("tag-id");
            $(this).val("");
            $(".current-list-tag").removeClass("current-list-tag");
            if (tagText)
                addTagBtn(tagText, $(this).data("tags-div"));
            let tagsId = JSON.parse($("#tags-input").val());
            tagsId.push(tagId)
            console.log(tagsId);
            $("#tags-input").val("[" + tagsId.toString() + "]");
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


    $(".remove-tag-btn ,.remove-cate-btn").click(function (e) {
        console.log("test");
        $(this).parent().addClass("remove-grid-item");
        let clicked = this;
        function aniCallBack() {
            $(clicked).parent().css("display", "none");

        }
        let aniTimeOut = setTimeout(aniCallBack, 185);
    });
    $(".del-cate-btn").click(deleteCateBtn);
    $(".ban-user-btn").click(banUserBtn);
    $(".cate-select").change(onCateSelectChange);
    $(".add-cate-btn").click(addCateBtnClick);
    $(".del-cho-btn").click(deleteChoiceBtn);
    $(".add-cho-btn").click(addChoiceBtn);
    $("#add-RL-btn").click(function (e) {
        e.preventDefault();
        addPollItem("RL");
    });
    $("#add-CL-btn").click(function (e) {
        e.preventDefault();
        addPollItem("CL");
    });
    $(".del-poll-item").click(delPollItem)
    $(".mov-poll-item").hover(enablePollMove, disablePollMove);
    let currentPollItem;
    $(".polls-items").click(function (e) { 
        e.preventDefault();
        console.log(e.pageX,e.pageY);
        console.log($(this).children().first().offset().left);
        console.log($(this).children().first().offset().top);
        // $(selector).();
    });
    $(".poll-item").on("dragstart", function () {
        $(this).addClass("poll-item-draging");
    
    });

    $(".poll-item").on("dragend", function () {
        $(this).removeClass("poll-item-draging");
    });
    $("#polls-items").on("dragover", function (e) {
        e.preventDefault();
        $(currentPollItem).after($.find(".poll-item-draging"));
        getCurrentIteM(e.pageX,e.pageY)
    }
    );

    $(".del-table-item").click(deleteTableItem);
}
);
function CategoryListClick(e) {
    if (!$(this).hasClass("active")) {
        $(this).addClass("active");
        $(this).siblings().removeClass("active");
        let subs = $(this).data("sub");
        let nextList = $(this).closest(".list-col").next(".list-col").find(".categories-list");
        $(this).closest(".list-col").nextAll(".list-col").map(function () {
            $(this).find(".categories-list").text('');
        }
        );
        if (subs)
            subs.forEach(element => {
                let cateLi = document.createElement('li');
                $(cateLi).addClass(["list-group-item", "category-list-item"]);
                $(cateLi).attr("data-sub", JSON.stringify(element['sub']));
                $(cateLi).attr("data-cate-id", element['id']);
                let spanName = document.createElement("span");
                $(spanName).text(element['name']);
                $(spanName).addClass("category-name");
                $(cateLi).append(spanName);
                let deleteBtn = document.createElement("button");
                $(deleteBtn).addClass(["btn ", "btn-app", "cus-btn-app", "btn-app-sm ", "float-right","cate-opt-btn", "del-cate-btn"]);
                //  data-lvl="2" data-toggle="modal" data-target="#add-cate-modal"

                $(deleteBtn).attr("data-lvl", "2");
                $(deleteBtn).attr("data-toggle", "modal");
                $(deleteBtn).attr("data-target", "#del-cate-modal");
                $(deleteBtn).append('<i class="far fa-trash-alt btn-app-icon"></i>Delete');
                $(deleteBtn).click(deleteCateBtn);
                $(cateLi).append(deleteBtn);
                let editBtn=document.createElement('button');
                $(editBtn).addClass(["btn ", "btn-app", "cus-btn-app", "btn-app-sm ", "float-right","cate-opt-btn", "del-cate-btn"]);
                $(editBtn).attr("data-lvl", "2");
                $(editBtn).attr("data-toggle", "modal");
                $(editBtn).attr("data-target", "#edit-cate-modal");
                $(editBtn).append('<i class="fas fa-pen btn-app-icon"></i>Edit');
                $(editBtn).click(editCateBtn)
                $(cateLi).append(editBtn);
                $(cateLi).click(CategoryListClick);
                
        
                $(nextList).append(cateLi);
            });
        $(nextList).children().first().click();
    }
}

// var listToAddId;
function addCateClick(e) {
    let prevLiActId = $(this).closest(".list-col").prev(".list-col").find(".categories-list").find(".active").data("cate-id");
    let lvl = $(this).data("lvl");
    if (lvl == '1') {
        prevLiActId = '-1';
    }
    $("#add-cate-id").val(prevLiActId);
    $("#add-cate-lvl").val(lvl)


}

function addTagBtn(tagText, tagsDivId) {
    let buttonTag = document.createElement("a");
    $(buttonTag).addClass(["btn", "btn-outline-info", "btn-tag", "item-grid-ani-100", "btn-tag-removeable"]);
    $(buttonTag).text(tagText);
    let removeBtn = document.createElement("div");
    $(removeBtn).addClass(["btn", "remove-tag-btn"]);
    $(removeBtn).append("<i class=\"fas fa-times\"></i>");
    $(buttonTag).append(removeBtn);
    $(tagsDivId).append(buttonTag);
    $(removeBtn).click(function (e) {
        $(this).parent().addClass("remove-grid-item");
        let clicked = this;
        function aniCallBack() {
            $(clicked).parent().css("display", "none");

        }
        let aniTimeOut = setTimeout(aniCallBack, 185);
    });
    addedTags.push(tagText);
}
function deleteCateBtn() {
    $("#del-cate-id").val($(this).parent().data("cate-id"));
    $("#del-cate-name").text($(this).prevAll(".category-name").text());
}
function editCateBtn(){
    $("#edit-cate-id").val($(this).parent().data("cate-id"));
    $('#edit-cate-name').val($(this).siblings('.category-name').text())
}

function deleteTagBtn() {
    $("#del-tag-id").val($(this).data("tag-id"));
    $("#del-tag-name").text($(this).data("tag-name"));
}
function banUserBtn() {
    $("#ban-user-name").text($(this).data("user-name"));
    $("#ban-user-id").val($(this).data("user-id"));
}
function onCateSelectChange() {
    $(this).parentsUntil(".row").last().nextAll(".cate-sel-col").css("visibility", "hidden");
    if (!parseInt($(this).val()) == 0)
        $(this).parentsUntil(".row").last().next(".cate-sel-col").css("visibility", "visible");
    let nextSelect = $(this).parentsUntil(".row").last().next(".cate-sel-col").find(".cate-select");
    let subs = $(this).find("[value=" + $(this).val() + "]").data("sub");
    $(nextSelect).html("");

    let allOpt = document.createElement("option");
    $(allOpt).text("All");
    $(allOpt).val("0");
    $(nextSelect).append(allOpt);
    try {
        subs.forEach(element => {
            let opt = document.createElement("option");
            $(opt).text(element['name']);
            $(opt).val(element['id']);
            $(opt).attr("data-sub", JSON.stringify(element['sub']));
            $(nextSelect).append(opt);
        });
    } catch (e) { }
}
function addCateBtnClick() {
    let cateName = null;
    let cateId = null;

    $(".cate-selectes .cate-sel-col:visible").find(".cate-select").map(function () {
        if (parseInt($(this).val()) <= 0) {
            if ($(this).parentsUntil(".row").last().prev(".cate-sel-col").length) {
                let prevSel = $(this).parentsUntil(".row").last().prev(".cate-sel-col").find(".cate-select");
                cateId = prevSel.val();
                cateName = prevSel.find("[value=" + cateId + "]").text();
            }
        }
    }
    );
    if (!cateId) {
        cateId = 0;
        cateName = "All"
    }
    // console.log(cateId);
    // console.log(cateName);
    let catesId = JSON.parse($("#cates-input").val());
    console.log(typeof catesId);
    if (!(cateId in catesId)) {
        let buttonTag = document.createElement("a");
        $(buttonTag).addClass(["btn", "btn-light", "cate-grid-item", "cate-item-removeable", "item-grid-ani-100"]);
        $(buttonTag).text(cateName);
        let removeBtn = document.createElement("div");
        $(removeBtn).addClass(["btn", "remove-cate-btn"]);
        $(removeBtn).append("<i class=\"fas fa-times\"></i>");
        $(buttonTag).append(removeBtn);
        $("#cate-div-ol").append(buttonTag);
        $(removeBtn).click(function (e) {
            $(this).parent().addClass("remove-grid-item");
            let clicked = this;
            function aniCallBack() {
                $(clicked).parent().css("display", "none");

            }
            let aniTimeOut = setTimeout(aniCallBack, 185);
        });
        catesId.push(cateId);
        $("#cates-input").val("[" + catesId.toString() + "]")

    }
}
function deleteChoiceBtn() {
    $(this).parent().remove();
}
function addChoiceBtn() {

    let choLi = document.createElement("li");
    $(choLi).addClass("poll-choies");
    let input = document.createElement("input");
    $(input).addClass(["form-control", "choies-inp"]);
    $(input).attr("type", "text");
    $(input).attr("placeholder", "Option..");
    let btn = document.createElement("button");
    $(btn).addClass(["btn ", "btn-app ", "btn-app-xs ", "del-cho-btn"]);
    $(btn).append('<i class="far fa-trash-alt btn-app-icon del-cho-btn"></i>');
    $(btn).click(deleteChoiceBtn);
    $(choLi).append(input);
    $(choLi).append(btn);
    $(this).prevAll(".poll-choesies").append(choLi);

}
function addPollItem(itemtype) {
    let item = document.createElement("div");
    $(item).addClass("poll-item");
    let movBtn=document.createElement("button");
    $(movBtn).addClass(["btn","mov-poll-item"]);
    $(movBtn).append(`<i class="fas fa-arrows-alt"></i>`);
    $(movBtn).hover(enablePollMove, disablePollMove);
    
    $(item).append(movBtn);
    let delBtn = document.createElement("button");
    $(delBtn).addClass(["btn", "del-poll-item"]);
    $(delBtn).append('<i class="far fa-times-circle"></i>');
    $(delBtn).click(delPollItem);
    $(item).append(delBtn);
    let title = document.createElement("h6");
    $(title).addClass(["float-right", 'poll-item-title']);
    if (itemtype == "CL")
        $(title).text("CheckBox List");
    else
        $(title).text("Radio List");

    $(item).append(title);

    let typeInp = document.createElement("input");
    $(typeInp).attr("type", "hidden");
    $(typeInp).attr("name", "item-type");
    $(typeInp).val(itemtype);
    let textarea = document.createElement("textarea");
    $(textarea).addClass(["form-control", "polls-que"]);
    $(textarea).attr("placeholder", "question text...");
    $(item).append(textarea);
    let ul = document.createElement("ul");
    $(ul).addClass("poll-choesies");
    let choLi = document.createElement("li");
    $(choLi).addClass("poll-choies");
    let input = document.createElement("input");
    $(input).addClass(["form-control", "choies-inp"]);
    $(input).attr("type", "text");
    $(input).attr("placeholder", "Option..");
    let btn = document.createElement("button");
    $(btn).addClass(["btn ", "btn-app ", "btn-app-xs ", "del-cho-btn"]);
    $(btn).append('<i class="far fa-trash-alt btn-app-icon del-cho-btn"></i>');
    $(btn).click(deleteChoiceBtn);
    $(choLi).append(input);
    $(choLi).append(btn);
    for (let i = 0; i < 4; i++)
        $(ul).append(choLi);
    $(item).append(ul);
    let addChoBtn = document.createElement("button");
    $(addChoBtn).addClass(['btn', 'btn-outline-primary', "float-right", "add-cho-btn"]);
    $(addChoBtn).text("Add Choice");
    $(addChoBtn).click(addChoiceBtn);
    $(item).append(addChoBtn);
    $(item).on("dragstart", function () {
        $(this).addClass("poll-item-draging");
    
    });

    $(item).on("dragend", function () {
        $(this).removeClass("poll-item-draging");
    });
    $("#polls-items").append(item);
}
function delPollItem() {
    $(this).parent().remove();
}
function enablePollMove() {
    $(this).parent().attr("draggable", "true");
}
function disablePollMove() {
    $(this).parent().attr("draggable", "false");
}

function getCurrentIteM(x,y){
    $(".poll-item").map( function (elementOrValue, indexOrKey) {
        var offset = $(this).offset();
        let xs = offset.left;
        let xe = xs +$(this).width();
        let ys = offset.top;
        let ye = ys + $(this).height();
        // console.log(...$.find(".poll-item-draging"));
        if(x>xs&&x<xe&&y>ys&&y<ye){
            // console.log($(...$.find(".poll-item-draging")).prev().get(0));
            // console.log($(this));
            if(this ==$(...$.find(".poll-item-draging")).prev().get(0))
                $(this).before($.find(".poll-item-draging"));
            else
                $(this).after($.find(".poll-item-draging"));
        }
    });


}

function deleteTableItem(){
    $("#del-id-span").text($(this).data("tid"));
    $("#del-id-inp").val($(this).data("tid"));
}

function onCategorySelectChange(){
    subs=($(this).find(`option[value="${$(this).val()}"]`).data('sub'));
    $(this).parent().nextAll(".col-2").css("visibility", "hidden");
    nextSelect=$(this).parent().next(".col-2").find(".category-select");
    nextSelect.parent().css("visibility", "visible")
    $(nextSelect).html(`
    <option data-sub="[]" value="0">All</option>
    
    `);
    if(subs){
        for (const item of subs) {
            // console.log(item);
            $(nextSelect).append(`
               <option data-sub='${JSON.stringify(item.sub)}' value="${item.id}">${item.name}</option>
            
            `);
        }        
    }
}


function editTagBtn(){
    $('#edit-tag-id').val($(this).data('tag-id'));
    $('#edit-tag-name').val($(this).parent().prev().prev().text());
    $('#edit-tag-desc').val($(this).parent().prev().text());
}