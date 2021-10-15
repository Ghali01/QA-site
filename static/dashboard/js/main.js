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
    $('#search-tags').keyup(searchTags);
    $('#search-users').keyup(searchUsers);
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
    
    $("#que-tags-input").keypress(e => {
        if (e.which == 13)
            e.preventDefault();
    });
    $("#que-tags-input").keydown(function (e) {

        if (e.which == 38 || e.which == 40)
            e.preventDefault();
        else if (e.which == 13) {
            let tagText = $(".current-list-tag").last().text();
            // console.log($(".current-list-tag"));
            let tagId = $(".current-list-tag").last().data("tag-id");
            $(this).val("");
            $(".current-list-tag").removeClass("current-list-tag");
            if (tagText)
                addTagBtn(tagText, tagId, $(this).data("tags-div"));
            let tagsId = JSON.parse($("#tags-input").val());
            tagsId.push(tagId)
            $("#tags-input").val(JSON.stringify(tagsId)).trigger('change');

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
            let tagsId = JSON.parse($("#tags-input").val());
            if (!$(this).text().startsWith($("#que-tags-input").val()) || tagsId.includes($(this).data('tag-id')))
                $(this).css('display', 'none');
            else {
                found++;
                $(this).css('display', 'block');

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
                currentPos = found;
                let lis = [...$(this).next().children()].reverse();
                let lastOne = undefined;
                for (let liTag of lis) {
                    if ($(liTag).css('display') == 'block') {
                        lastOne = liTag;
                        break;
                    }
                }
                $(lastOne).addClass("current-list-tag");
            }
            else {
                $(hasHover).removeClass("current-list-tag");
                let lis = [...$(hasHover).prevAll()].reverse();
                let lastOne = undefined;
                for (let liTag of lis) {
                    if ($(liTag).css('display') == 'block') {
                        lastOne = liTag;
                        break;
                    }
                }
                $(lastOne).addClass("current-list-tag");
                currentPos--;

            }

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
                let lis = [...$(this).next().children()];
                let firstOne = undefined;
                for (let liTag of lis) {
                    if ($(liTag).css('display') == 'block') {
                        firstOne = liTag;
                        break;
                    }
                }
                $(firstOne).addClass("current-list-tag");
            }
            else {

                $(hasHover).removeClass("current-list-tag");
                let lis = [...$(hasHover).nextAll()];
                let firstOne = undefined;
                for (let liTag of lis) {
                    if ($(liTag).css('display') == 'block') {
                        firstOne = liTag;
                        break;
                    }
                }
                $(firstOne).addClass("current-list-tag");
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

        let tagText = $(this).text();
        let tagId = $(this).data("tag-id");
        let tagsId = JSON.parse($("#tags-input").val());
        tagsId.push(tagId)
        $("#tags-input").val(JSON.stringify(tagsId)).trigger('change');
        addTagBtn(tagText, tagId, $(this).parent().data("tags-div"));
        $(this).parent().css({ display: 'none' });
    });
    // tag list end


    $(".remove-tag-btn ,.remove-cate-btn").click(removeTagBtn);
    $(".del-cate-btn").click(deleteCateBtn);
    $(".ban-user-btn").click(banUserBtn);
    $(".cate-select").change(onCateSelectChange);
    // $(".cate-select").trigger('');
    $(".add-cate-btn").click(addCateBtnClick);
    $(".del-cho-btn").click(deleteChoiceBtn);
    $(".add-cho-btn").click(addChoiceBtn);
    $("#add-RL-btn").click(function (e) {
        e.preventDefault();
        addPollItem("R");
    });
    $("#add-CL-btn").click(function (e) {
        e.preventDefault();
        addPollItem("C");
    });
    $(".del-poll-item").click(delPollItem)
    $(".mov-poll-item").hover(enablePollMove, disablePollMove);
    let currentPollItem;
    $(".polls-items").click(function (e) { 
        e.preventDefault();
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
    $('.toggle-post-pub-btn').click(togglePubPost);
    $('.edit-sug-item-btn').click(editSuggestedItem);

    $(".del-li-btn").click(deleteLiBtn);
    $('#target-type').change(targetTypeSelect);
    $('.remove-report-btn').click(removeReports);
    $('.save-poll-btn').click(savePollBtn);
    $('.pub-poll-btn').click(pubPollBtn);
    $('.tog-open-btn').click(toggOpenPollBtn);
    $('.pub-poll-btn-t').click(pubPollBtnT);
    $('#reasons-select').change(selectReason);
    $('.toggle-que-ex-btn').click(toggExamQue);
    $('.mark-ans-exam-btn').click(markCorrectAnswer);
    $('#restart-input').keyup(restartInputWrite);
    $('#restart-btn').click(restratBtn);
    $('#add-a-i-btn').click(addAuthItem);
    $('#sav-l-auth').click(saveListAuth);
    $('.del-auth-item').click(deleteAuthItem);
    let now= new Date(),
    dateNextWeek=new Date(now.getTime()+(1000*60*60*24*7));

    document.cookie=`utcOffset=${ -1*(now.getTimezoneOffset()/60)}; expires=${dateNextWeek.toGMTString()}; path=/`;
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
                $(deleteBtn).append(`<i class="far fa-trash-alt btn-app-icon"></i>${gettext('Delete')}`);
                $(deleteBtn).click(deleteCateBtn);
                $(cateLi).append(deleteBtn);
                let editBtn=document.createElement('button');
                $(editBtn).addClass(["btn ", "btn-app", "cus-btn-app", "btn-app-sm ", "float-right","cate-opt-btn", "del-cate-btn"]);
                $(editBtn).attr("data-lvl", "2");
                $(editBtn).attr("data-toggle", "modal");
                $(editBtn).attr("data-target", "#edit-cate-modal");
                $(editBtn).append(`<i class="fas fa-pen btn-app-icon"></i>${gettext("Edit")}`);
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

function addTagBtn(tagText, tagId, tagsDivId) {
    let buttonTag = document.createElement("button");
    $(buttonTag).addClass(["btn", "btn-outline-info", "btn-tag", "item-grid-ani-100", "btn-tag-removeable"]);
    $(buttonTag).attr("type", "button");
    $(buttonTag).text(tagText);
    $(buttonTag).data('tag-id', tagId);
    let removeBtn = document.createElement("div");
    $(removeBtn).addClass(["btn", "remove-tag-btn"]);
    $(removeBtn).append("<i class=\"fas fa-times\"></i>");
    $(buttonTag).append(removeBtn);
    $(tagsDivId).append(buttonTag);

    $(removeBtn).click(removeTagBtn);
    if ($(tagsDivId).hasClass('filter-tags-div'))
        $(buttonTag).click(removeSearchTag);
}

function removeTagBtn(e) {
    let tagId = $(this).parent().data('tag-id');
    let tagsId = JSON.parse($("#tags-input").val());
    tagsId.splice(tagsId.indexOf(tagId));
    $("#tags-input").val(JSON.stringify(tagsId)).trigger('change');

    $(this).parent().addClass("remove-grid-item");
    let clicked = this;
    function aniCallBack() {
        $(clicked).parent().remove();
        // $(clicked).parent().css("display","none");

    }
    let aniTimeOut = setTimeout(aniCallBack, 185);
}


function deleteCateBtn() {
    $("#del-cate-id").val($(this).parent().data("cate-id"));
    $("#del-cate-name").text($(this).prevAll(".category-name").text());
}
function editCateBtn(){
    $("#edit-cate-id").val($(this).parent().data("cate-id"));
    $("#edit-cate-desc").val($(this).parent().data("cate-desc"));
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
    console.log($(this).val());
    let subs = $(this).find(`[value= ${$(this).val()} ]`).data("sub");
    $(nextSelect).html("");

    let allOpt = document.createElement("option");
    $(allOpt).text(gettext("Select Category"));
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

    $(this).parentsUntil('.row').parent().find('#category-id').val($(this).val());
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

    if (itemtype == "C")
        $(title).text(gettext("CheckBox List"));
    else
        $(title).text(gettext("Radio List"));

    $(item).append(title);
    let typeInp = document.createElement("input");
    $(typeInp).attr("type", "hidden");
    $(typeInp).attr("name", "item-type");
    $(typeInp).addClass('item-type');
    $(typeInp).val(itemtype);
    $(item).append(typeInp);
    let textarea = document.createElement("textarea");
    $(textarea).addClass(["form-control", "polls-que"]);
    $(textarea).attr("placeholder", gettext("question text..."));
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
    $(addChoBtn).text(gettext("Add Choice"));
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

    $('#add-cate-id').val($(this).val());
    subs=($(this).find(`option[value="${$(this).val()}"]`).data('sub'));
    $(this).parent().nextAll(".col-2").css("visibility", "hidden");
    nextSelect=$(this).parent().next(".col-2").find(".category-select");
    nextSelect.parent().css("visibility", "visible")
    $(nextSelect).html(`
    <option data-sub="[]" value="0">${gettext('All')}</option>
    
    `);
    if(subs){
        for (const item of subs) {
            // console.log(item);
            $(nextSelect).append(`
               <option data-sub='${JSON.stringify(item.sub)}' value="${item.id}">${item.name}</option>
            
            `);
        }        
    }
    getCategoryTags($(this).val());
    }
function getCategoryTags(id){
    $("#tags-table").html('');
    $.get(jsonTagsUrl+"?cate-id="+id, {},
        function (data, textStatus, jqXHR) {
            despalyTags(data);
        },
    );
}
function searchTags(){
    $("#tags-table").html('');
    let searchText=$(this).val();
    let _this=this;
    $.get(jsonTagsSearchUrl+`?search-text=${searchText}&cate-id=${$('#add-cate-id').val()}`, {},
        function (data, textStatus, jqXHR) {
    
            if ($(_this).val()==searchText)
                despalyTags(data);
        },
    );
}
        
function despalyTags(tags){
    tags=JSON.parse(tags);
    $("#tags-table").html('');
            
    for (let item of tags ){
        let tr=document.createElement('tr');
        $(tr).html(`
        <td>${item.name}</td>
        <td>${item.description}<td>
            <button class="btn btn-app cus-btn-app d-block del-tag-btn" data-lvl="2" data-toggle="modal" data-target="#del-tag-modal"
            data-tag-id="${item.id}" data-tag-name="${item.name}">
                <i class="far fa-trash-alt btn-app-icon"></i>${gettext('Delete')}
            </button>
            <button class="btn btn-app cus-btn-app d-block edit-tag-btn" data-lvl="2" data-toggle="modal" data-target="#edit-tag-modal"
            data-tag-id="${item.id}">
                <i class="fas fa-pen btn-app-icon"></i>${gettext('Edit')}
            </button>
        </td>
   
        `);
        $(tr).find(".edit-tag-btn").click(editTagBtn);
        $(tr).find(".del-tag-btn").click(deleteTagBtn);
        $("#tags-table").append(tr);
    }
}
function editTagBtn(){
    $('#edit-tag-id').val($(this).data('tag-id'));
    $('#edit-tag-name').val($(this).parent().prev().prev().text());
    $('#edit-tag-desc').val($(this).parent().prev().text());
}

var searchVal='';
function searchUsers(){
    if ($(this).val()==searchVal)
        return
    searchVal=$(this).val();
    $('#users').html('');
    if($(this).val()){
        let searchText=$(this).val(),_this=this;
    $.get(`${searchUserLink}?search-text=${searchText}`, {},
        function (data, textStatus, jqXHR) {
            if(searchText==$(_this).val())
            {     
                $('#users').html('');
                let users=JSON.parse(data);
                for (let user of users){
                    let tr=document.createElement('tr');
                    $(tr).html(`
                    <td>
                    ${user.userName}
                  </td>
                  <td>${user.fullName}</td>
                  <td>${user.id}</td>
                  <td>${user.email}</td>
                  <td>${user.perm}</td>
                  <td>
                    <div class="actions-btns" data-item-id="${user.id}" data-user-name="${user.userName}">

                      <a class="btn btn-app cus-btn-app" href="/profile/${user.id}">
                        <i class="fas fa-user btn-app-icon"></i>Profile
                      </a>
                      <a class="btn btn-app cus-btn-app app-btn-70" href="/profile/user-questions/${user.id}">
                        <i class="fas fa-external-link-alt btn-app-icon"></i>${gettext('Questions')}
                      </a>
                      <a class="btn btn-app cus-btn-app app-btn-70" href="/profile/user-answers/${user.id}">
                        <i class="fas fa-angle-right btn-app-icon"></i>${gettext('Answers')}
                      </a>
                      <a class="btn btn-app cus-btn-app app-btn-70" href="/dashboard/templates/${user.language.toUpperCase()}?to=${user.email}">
                        <i class="far fa-envelope btn-app-icon"></i>${gettext('Email')}
                      </a>
                      ${user.isBaned!='True'?`<button class="btn btn-app cus-btn-app ban-user-btn"
                      data-toggle="modal" data-lvl="2" data-target="#ban-modal"
                      >
                        <i class="fas fa-user-slash btn-app-icon"></i>${gettext('Ban')}
                      </button>`:
                      `
                      <button class="btn btn-app cus-btn-app unban-user-btn"
                      data-toggle="modal" data-lvl="2" data-target="#unban-modal"
                      >
                        <i class="fas fa-user btn-app-icon"></i>${gettext('unban')}
                      </button>`}
                      <button class="btn btn-app cus-btn-app app-btn-70 prune-btn"
                      data-toggle="modal" data-lvl="2" data-target="#prune-modal"
                      >
                        <i class="far fas fa-user-minus btn-app-icon"></i>${gettext('Prune')}
                      </button>
                      <button class="btn btn-app cus-btn-app app-btn-80 permission-btn" data-lvl="2" data-toggle="modal" data-target="#permissions-modal">
                        <i class="fas fa-address-card btn-app-icon"></i>${gettext('Permissions')}
                      </button>
                    </div>
                  </td>
             
                    `);
                    $(tr).find('.permission-btn').click(premissionBtnClick);
                    $(tr).find('.prune-btn').click(pruneBtnClick);
                    $(tr).find('.ban-user-btn').click(banUserBtn);
                    $(tr).find('.unban-user-btn').click(unbanUserBtn);
                    $('#users').append(tr);
                }
            }
      },
    );
}
}
function banUserBtn() {
    $('#ban-user-name').text($(this).parent().data('user-name'));
    $('#ban-user-id').val($(this).parent().data('item-id'));
}
function unbanUserBtn() {
    $('#unban-user-name').text($(this).parent().data('user-name'));
    $('#unban-user-id').val($(this).parent().data('item-id'));
}

function  premissionBtnClick(){
    $('#prem-user-id').val($(this).parent().data('item-id'));
}

function  pruneBtnClick(){
    $('#prune-user-id').val($(this).parent().data('item-id'));
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




function togglePubPost() {
    let clicked=this;
    $.post("/dashboard/togg-pub-post", 
    {
        csrfmiddlewaretoken:getCookie('csrftoken'),
        'post-id':$(this).data('post-id')
    }
    ,
        function (data, textStatus, jqXHR) {
            if(data=='pub'){
                $(clicked).html(`<i class="fas fa-eye-slash btn-app-icon"></i>${gettext('Unpublish')}`);
            }
            else if (data=='unpub'){
                $(clicked).html(`<i class="fas fa-eye btn-app-icon"></i>${gettext('Publish')}`);

            }
        },
    );
}

function editSuggestedItem() {
    $('#cate-name').val($(this).parent().data('name'));
    $('#cate-desc').val($(this).parent().data('desc'));
    $('#item-id').val($(this).parent().data('item-id'));
}

function deleteLiBtn() {
    $("#del-id").val($(this).parent().data("item-id"));
    $("#del-name").text($(this).prevAll(".li-name").text());
  }



function targetTypeSelect(){
    let targets=undefined;
    if($(this).val()=='C')
        targets=$(this).data('categories');
    else if ($(this).val()=='T')
       targets=$(this).data('tags');
    $('#targets').html('');
    if(targets)
        targets.forEach(el=>$('#targets').append(`<option value="${el.id}">${el.name}</option>`));
}

function removeReports() { 
    let clicked=this;
    $.post("/dashboard/remove-reports", 
    {
        csrfmiddlewaretoken:getCookie('csrftoken'),
        'type':$(this).data('type'),
        'reason-id':$(this).data('reason-id'),
        'report-on':$(this).data('report-on'),
    }
    ,
        function (data, textStatus, jqXHR) {
            if (data=='done')
                $(clicked).parentsUntil('tbody').remove();
        },
    );
 
}

function collectPollItems(){
    let data=[];

    [...$('.poll-item')].forEach(function(el){
        let item={
            type:$(el).find('.item-type').val(),
            text:$(el).find('.polls-que').val()
        };
        let options=[];
        [...$(el).find('.poll-choies')].forEach(function(el){
            if($(el).find('.choies-inp').val())
              options.push(($(el).find('.choies-inp').val()));
        });
        item['options']=options;
        data.push(item);
    });  
    $('#poll-items').val(JSON.stringify(data));
}
function savePollBtn(){
    collectPollItems();
    $('#pub-poll-inp').remove();
    $('#poll-form').submit();
}
function pubPollBtn(){
    collectPollItems();
    $('#poll-form').submit();
}

function toggOpenPollBtn(){
    let clicked=this;
    $.post("/dashboard/togg-poll-open",{
        csrfmiddlewaretoken:getCookie('csrftoken'),
        'poll-id':$(this).data('poll-id')
    },
        function (data, textStatus, jqXHR) {
            if(data=='opened')
                $(clicked).html(`<i class="fas fa-lock btn-app-icon"></i>${gettext('Lock')}`);
            if(data=='closed')
                $(clicked).html(`<i class="fas fa-unlock btn-app-icon"></i>${gettext('Unlock')}`);
            },
    );
}
function pubPollBtnT() { 
    let clicked=this;
    $.post("/dashboard/pub-poll",{
        csrfmiddlewaretoken:getCookie('csrftoken'),
        'poll-id':$(this).data('poll-id')
    },
        function (data, textStatus, jqXHR) {
            if(data=='done'){
                $(clicked).siblings('.tog-open-btn').html('<i class="fas fa-lock btn-app-icon"></i>Lock');
                $(clicked).remove();
                }
            },
    );

 }

 function selectReason(){
    if ($(this).data('general').includes($(this).val())){
        $('#target-type').val('G');
        $('#target-type').trigger('change');
        $('#target-type').attr('readonly',true);
    }
    else
        $('#target-type').attr('readonly',false);

}

function toggExamQue() {
    let clicked=this;
    $.post("/dashboard/togg-exam-que",
    {
        csrfmiddlewaretoken:getCookie('csrftoken'),
        'que-id':$(this).data('que-id')
    },
        function (data, textStatus, jqXHR) {
            if(data=='added'){
                $(clicked).html(` <i class="fas fa-eye btn-app-icon"></i>${gettext('Remvoe from exams')}`);
                window.open(`/dashboard/answers/1/${$(clicked).data('que-id')}`,'_blank')
            } else if (data=='removed')
                $(clicked).html(`<i class="fas fa-plus btn-app-icon"></i>${gettext('Add to exams')}`);
        },
    );
  }


function markCorrectAnswer() {
    let clicked=this;
    $.post("/dashboard/mark-correct-ans",
    {
        csrfmiddlewaretoken:getCookie('csrftoken'),
        'ans-id':$(this).data('ans-id')
    },
        function (data, textStatus, jqXHR) {
            if(data!='error'){
                data=JSON.parse(data);
                $('.correct-td').append(`
                <button data-ans-id="${data.id}" style="height: 70px;"  class="btn btn-app cus-btn-app app-btn-70 mark-ans-exam-btn">
                <i class="fas fa-check btn-app-icon"></i>${gettext('Mark as correct')}
              </button>
              `);
              $('.correct-td').parent().find('.mark-ans-exam-btn').click(markCorrectAnswer);
              $('.correct-td').removeClass('correct-td');
              $(clicked).parent().addClass('correct-td');
              $(clicked).remove();
        
            }
        },
    );
}


function restartInputWrite(){
    if($(this).val()=='yes'){
      $('#restart-btn').removeClass('btn-secondary');
      $('#restart-btn').addClass('btn-danger')
    } else{
      
      $('#restart-btn').addClass('btn-secondary');
      $('#restart-btn').removeClass('btn-danger')
    }
  }
  function restratBtn(e){
    if ($('#restart-input').val()!='yes')
      e.preventDefault()
  }

  
function addAuthItem(){
    let li =document.createElement('li');
    $(li).html(`
    <input type="text" class="form-control" >
    <button class="btn btn-default del-auth-item">
      <i class="fas fa-trash"></i>
    </button>
`);
    $(li).find('.del-auth-item').click(deleteAuthItem);
    $('#auth-list').append(li);
}

function saveListAuth(e){
    data=[];
    [...$('#auth-list').children()].forEach(e=>{
        if($(e).find('input').val())
            data.push($(e).find('input').val());
    });
    $('#auth-list-inp').val(JSON.stringify(data));
}
function deleteAuthItem(){
    $(this).parent().remove();
}