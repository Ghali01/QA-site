
var addedTags = [];
var editor;
var searchText = '';
$(document).ready(
    // animation for forms start
    function () {
        // $('.column-no-border').parent().css('border', 'none');
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
            if (!$(this).hasClass("down-icon-a")) {
                $(this).css("animation-name", "none");
                $(this).css("animation-name", "down-icon-ani");

            } else {
                $(this).css("animation-name", "none");
                // $(this).css("animation-direction","reverse");
                $(this).css("animation-name", "down-icon-ani2");

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
        $('.share-btns').click(function (e) {
            e.stopPropagation();
            
        });
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
            $('.share-btns.showed').css({ display: "none" });
            $('.share-btns.showed').removeClass('showed');

            $('.nav-drop-down.opend').animate({
                top: '22px',
                opacity: 0,

            }, 300, function () {
                $('.nav-drop-down').removeClass('opend');
                $('.nav-drop-down').hide();

            });
        });
        $(".custom-select").click(function (event) {
            event.stopPropagation();
        });
        $(".tags-list").click(function (event) {
            event.stopPropagation();
        });
        $(".nav-drop-down").click(function (event) {
            event.stopPropagation();
        });
        $(".custom-select-item").click(customSelected);
        // custom select end
        //editor start
        if (document.getElementById("editor") != undefined) {
            // tinyMDE = new TinyMDE.Editor({ element: 'editor', content: "" });
            // var commandBar = new TinyMDE.CommandBar({ element: 'editor-toolbar', editor: tinyMDE });
            try{
            const Editor = toastui.Editor;
            editor = new Editor({
                el: document.querySelector('#editor'),
                // height: '300px',
                autofocus:false,
                initialValue: $('#editor').data('init-val'),
                theme: 'dark',
                initialEditType:'wysiwyg'
              });
              $('.ProseMirror ').addClass('custom-scrollbar');
              document.querySelectorAll('.post-content pre code').forEach((el) => {
                $(el).html($(el).html().trim());
                hljs.highlightElement(el);
              });
            }catch(e){

            }
            }

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
            $("#reg-form .form-input:not(.no-req)").map(function () {
                if (!$(this).val() && !$(this).next().hasClass("r-error-span")) {
                    $(this).next().find(".error-val").text(gettext("This Field is required"));
                    $(this).next().slideDown();
                    isEmpyty = true;
                    $(this).focus(function () {
                        $(this).next().slideUp();

                    });
                }

            });
            if (isEmpyty) {
                e.preventDefault();
            } else if ($("#email-input").length>0&&!emailPatt.test($("#email-input").val())) {
                $("#email-input").next().find(".error-val").text(gettext("Email not valid"));
                $("#email-input").next().slideDown();
                e.preventDefault();

            }
            else if ($("#password-input").val().length < 8) {
                $("#password-input").next().find(".error-val").text(gettext("Password should be 8 charters or more"));
                $("#password-input").next().slideDown();
                e.preventDefault();

            }
            else if ($("#password-input").val() != $("#confirmPassword-input").val()) {
                $("#confirmPassword-input").next().find(".error-val").text(gettext("Password does not match"));
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
            $($(this).data("content")).css("display", "block");
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
                $(this).find(".num-in-tb").css("border-right", "1px solid #fff");
            }, function () {
                // out
                $(this).find(".num-in-tb").css("border-right", "inherit");

            }
        );
        // side list start
        $(".side-list-item").click(function () {
            $(this).siblings().removeClass("side-list-item-act");
            $(this).addClass("side-list-item-act");
            $($(this).data("content-p") + " .side-list-content").css("display", "none");
            $($(this).data("content-p") + " " + $(this).data("content")).css("display", "block");
        })
        // side list end

        $(".remove-tag-btn").click(removeTagBtn);
        $(".add-comment-span").click(showCommentDiv);
        $(" .category-select-toolbar .custom-select-item , .categoriis-lists .custom-select-item").click(onSelectCategory)


        $(".btn.tag-star").click(togTagToFav);


        $('.nav-drop-down').hide();

        $('#drop-d-btn-nav').click(function (e) {
            if (!$('.nav-drop-down').hasClass('opend')) {
                $('.nav-drop-down').show();
                $('.nav-drop-down').animate({
                    top: '50px',
                    opacity: 1,

                }, 300, function () {
                    $('.nav-drop-down').addClass('opend')

                });
            } else {

                $('.nav-drop-down').animate({
                    top: '22px',
                    opacity: 0,

                }, 300, function () {
                    $('.nav-drop-down').removeClass('opend')
                    $('.nav-drop-down').hide();
                });
            }
        });

        if (location.pathname == '/login' || location.pathname == '/register') {
            $.ajaxSetup({ cache: true });
            $.getScript('https://connect.facebook.net/en_US/sdk.js', function () {
                FB.init({
                    appId: '227023055931495',
                    version: 'v2.7' // or v2.1, v2.2, v2.3, ...
                });
                $('#fb-login-btn').click(fbLoginBtn);

            });
            $.getScript("https://accounts.google.com/gsi/client", function (script, textStatus, jqXHR) {
                $('#go-login-btn').click(function () {
                    $('#go-login-btn-api').find('[role=button]').click();
                });

            });
        }
        $('#gi-login-btn').click(githubLoginClick);
        $('.add-post-btn').click(postFormSubmit);
        $('.n-sub-list').slideUp(0);
        $('.n-sl-btn').click(function (e) {
            $(this).next().slideDown()
        });
        $('.filter li').click(filterChange);
        $('#mode-fil-btn').click(moderatorFilter)
        $('.filter-tags-div .btn-tag').click(removeSearchTag)
        $('.page-btn').click(pgClick);
        $('.chang-que-st-m-btn').click(changeQueStMod);
        $('.chang-anss-st-m-btn').click(changeAnswersStMod);
        $('.chang-ans-st-m-btn').click(changeAnswerStMod);
        $('.one-click-filter li').click(oneClickFilterChange);
        $('.sort-icon').click(voteBtnClick);
        $('.add-ans-button').click(addAnswerBtn);
        $('.add-ans-continer').slideUp(0);
        $('.see-more-btn-index').click(seeMoreIndex);
        $('.see-more-btn-tag-questions').click(seeMoreTagQuestions);
        $('.see-more-btn-tags').click(seeMoreTags);
        $('.loading-circle').hide();
        $('.button-filter button').click(btnFilterClick);
        $('.see-more-btn-add-que').click(seeMoreAddQue)
        $('#que-title').keyup(queTitleChange);
        $('.add-que-h-inp').change(queTitleChange);
        $('.add-comm-btn').click(addCommentBtn);
        $('.all-comment-span').click(seeAllComments);
        $('.chang-edit-st-m-btn').click(changeSugEditStatus);
        $('.see-more-btn-user-que').click(seeMoreUserQue);
        $('.search-usr-que').keyup(searchUsrQuestions);
        $('.see-more-btn-user-ans').click(seeMoreUserAns);
        $('.search-usr-ans').keyup(searchUsrAnswers);
        $('.add-comm-inp').keydown(function (e) {
            if (e.which === 13)
                $(this).next().trigger('click');
        });

        $('.fav-que-btn').click(favQueBtn);
        $('.flo-que-btn').click(folloUserQueBtn);
        $('.follow-btn').click(folloUserQueBtn);
        $('.see-more-btn-badges').click(seeMoreUserBadges);
        $('.see-more-btn-followers').click(seeMoreUserFollowers);
        $('.see-more-btn-favq').click(seeMoreFavQuestions);
        $('.report-btn').click(reportBtnClick);
        $('.search-nav-form .search-input').keydown(searchNavDown);
        $('.search-nav-form .search-input').keyup(searchNavUp);
        $('.search-nav-form .search-input').focus(_=>{
            if ($('.search-nav-form .search-resaults').children().length)
                $('.search-nav-form .search-resaults').show();
        });
        $('.search-nav-form .search-resaults').hide();
        $('.error-poll').slideUp(0);
        $('.submit-poll-btn').click(submitPoll);
        $(window).click(_=>{
            if(!$('.search-nav-form .search-input').is(':focus'))
                $('.search-nav-form .search-resaults').hide();
            // $('.search-nav-form .search-resaults').html('');
        
        });
        $('.custom-checkbox').click(customCheckInput);
        $('.custom-radiobox').click(customCheckInput);
        $('.custom-input-number').keydown(numInpDown);
        $('.share-btn').click(sharePop);
        $('.copy-lnk').click(copyLink);
        $("#myTextBox").inputFilter(function(value) {
            return /^\d*$/.test(value);    // Allow digits only, using a RegExp
          });        
          let now = new Date(),
        dateNextWeek = new Date(now.getTime() + (1000 * 60 * 60 * 24 * 7));

        document.cookie = `utcOffset=${-1 * (now.getTimezoneOffset() / 60)}; expires=${dateNextWeek.toGMTString()}; path=/`;
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
function onSelectCategory() {
    let parentC = $(this).parentsUntil(".category-select-toolbar").last().parent();
    parentC.data("cur-val", $(this).data("cate-id"));
    parentC.nextAll(".category-select-toolbar").css('visibility', 'hidden');
    parentC.next(".category-select-toolbar").css('visibility', 'visible');
    let subs = $(this).data("sub");
    let nextList = parentC.next(".category-select-toolbar").find(".custom-select-list");
    $(nextList).html('');
    if (subs)
        subs.forEach(element => {
            let cateLi = document.createElement('li');
            $(cateLi).addClass("custom-select-item");
            $(cateLi).attr("data-sub", JSON.stringify(element['sub']));
            $(cateLi).attr("data-cate-id", element['id']);
            $(cateLi).text(element["name"]);
            $(cateLi).click(customSelected);
            $(cateLi).click(onSelectCategory);

            $(nextList).append(cateLi);
        });

    let par = $(this).parentsUntil('.categoriis-lists').last().parent();
    $(par).find('#category-id').val($(this).data("cate-id")).trigger('change');
}
function customSelected() {
    $(this).parent().prev().text("");
    $(this).parent().prev().append("<span class=\"selected-span\">" + $(this).text() + "</span>");
    $(this).parent().prev().append("<i class=\"fas fa-caret-down select-arrow\"></i>")
    $(this).parent().css({
        visibility: "hidden"

    });
    $(this).parent().prev().toggleClass("btn-select-act");
}

function fbLoginBtn() {
    FB.login(function (response) {
        if (response.status == 'connected') {
            let form = $('#social-form')
            $(form).attr('method', 'POST');
            $(form).attr('action', '/facebook-login');
            $(form).append(`<input type="hidden" name="user-id" value="${response.authResponse.userID}">`);
            $(form).append(`<input type="hidden" name="token" value="${response.authResponse.accessToken}">`);
            $(form).submit();
        }
        else {
            $('#login-error').slideDown();
        }
    }, { scope: 'public_profile,email' });
}

function googleLoginCallback(response) {
    let form = $('#social-form')
    $(form).attr('method', 'POST');
    $(form).attr('action', '/google-login');
    $(form).append(`<input type="hidden" name="jwt" value="${response.credential}">`);
    $(form).submit();

}

function githubLoginClick() {
    location.href = `https://github.com/login/oauth/authorize?client_id=325f252be688f7172df1&scope=user&redirect_uri=${location.protocol}//${location.host}/github-login`;

}

var perventPostForm = true;
function postFormSubmit(e) {
    if (perventPostForm) {
        e.preventDefault();
    }
    $('#post-body').val(editor.getHTML());
    perventPostForm = false;
    $("#post-form").submit();
}

function filterChange() {

    $(this).parent().next('input').val($(this).data('value'));
    $(this).parent().prev('button').find('.selected-span').text($(this).text());
}


var filterInSearch = (filterObject) => {
    let searchText = '';
    for (let key in filterObject) {
        searchText += `${key}=${filterObject[key]}&`;
    }
    searchText = searchText.slice(0, -1);
    location.search = searchText;
}

function moderatorFilter() {
    let filterObject = {
        'category': $('#category-id').val().trim(),
        'order': $('#order-input').val(),
        'tags': $('#tags-input').val(),


    };
    if ($('#search-input').val())
        filterObject['search'] = $('#search-input').val();
    filterInSearch(filterObject);
}

function removeSearchTag() {
    let tagId = $(this).parent().data('tag-id');
    let tagsId = JSON.parse($("#tags-input").val());
    tagsId.splice(tagsId.indexOf(tagId));
    $("#tags-input").val(JSON.stringify(tagsId)).trigger('change');

    $(this).addClass("remove-grid-item");
    let clicked = this;
    function aniCallBack() {
        $(clicked).remove();
        // $(clicked).parent().css("display","none");

    }
    let aniTimeOut = setTimeout(aniCallBack, 185);

}

function pgClick() {
    path = location.pathname;
    path = path.slice(0, path.lastIndexOf('/') + 1)
    path += $(this).text();
    location.pathname = path;
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

function changeQueStMod() {
    let clicked = this;
    let item = $(this).parentsUntil('.await-item').parent();
    $.post("/moderators/change-suggested-question", {
        'csrfmiddlewaretoken': getCookie('csrftoken'),
        'que-id': $(this).data('que-id'),
        'status': $(this).data('action'),
    },
        function (data, textStatus, jqXHR) {
            if (data == 'done') {
                if (!$(clicked).hasClass('no-animate')) {

                    item.addClass('ani-await-item');
                    setTimeout(_ => $(item).remove(), 500);
                }
                else {
                    location.reload();
                }
            }
        },
    );
}
function changeAnswerStMod() {
    let clicked = this;
    let item = $(this).parentsUntil('.await-item').parent();
    $.post("/moderators/change-suggested-answer", {
        'csrfmiddlewaretoken': getCookie('csrftoken'),
        'ans-id': $(this).data('ans-id'),
        'status': $(this).data('action'),
    },
        function (data, textStatus, jqXHR) {
            if (data == 'done') {
                if (!$(clicked).hasClass('no-animate')) {

                    item.addClass('ani-await-item');
                    setTimeout(_ => $(item).remove(), 500);
                }
                else {
                    location.reload();
                }
            }
        },
    );
}

function changeAnswersStMod() {
    let clicked = this;
    let item = $(this).parentsUntil('.await-item').parent();
    $.post("/moderators/change-suggested-answers", {
        'csrfmiddlewaretoken': getCookie('csrftoken'),
        'que-id': $(this).data('que-id'),
        'status': $(this).data('action'),
        'mode': $(this).data('mode')
    },
        function (data, textStatus, jqXHR) {
            if (data == 'done') {
                if (!$(clicked).hasClass('no-animate')) {

                    item.addClass('ani-await-item');
                    setTimeout(_ => $(item).remove(), 500);
                }
                else {
                    location.reload();
                }
            }
        },
    );
}


function oneClickFilterChange() {
    let searchObject = {};
    [...$('.filter')].forEach(filter =>
        searchObject[$(filter).find('input').attr('name')] = $(filter).find('input').val()
    );
    // console.log(searchObject);
    filterInSearch(searchObject);
}


function voteBtnClick() {
    let type = $(this).hasClass('sort-icon-up') ? 'up' : 'down';
    let clicked = this;
    $.get("/post-vote", { 'type': type, 'post-id': $(this).data('post-id') },
        function (data, textStatus, jqXHR) {
            data = JSON.parse(data);
            if (data.resault == 'done') {
                $(clicked).siblings('.sort-icon').removeClass('sort-icon-act')
                $(clicked).addClass('sort-icon-act');
                $(clicked).siblings('.votes-number-span').text(data.votes);
            }
            else if (data.resault == 'undo') {
                $(clicked).removeClass('sort-icon-act');
                $(clicked).siblings('.votes-number-span').text(data.votes);
            }
        },
    );

}

function addAnswerBtn() {
    let _this = this;
    let f = function () {
        $('.add-ans-continer').slideDown();
        $(_this).off('click');
        $(_this).click(() => {
            $('#answer-body').val(editor.getHTML());
            $('#answer-form').submit();
        });
    }
    checkAuth(f)
}
var pageIndc = 1;
function seeMoreIndex() {
    $(this).next().show();
    let clicked = this;
    $.get(`/see-more/${pageIndc++}${$(this).data('category-id') ? '/' + $(this).data('category-id') : ''}` + location.search, {},
        function (data, textStatus, jqXHR) {
            $(clicked).next().hide();
            data = JSON.parse(data);
            if (parseInt(data.remPages) <= 0) {
                $(clicked).hide()
            }
            $(clicked).prev().append(data.html);
        },
    );
}

function seeMoreTagQuestions() {
    $(this).next().show();
    
    let clicked = this;
    $.get(`/see-more-tag-questions/${$(this).data('tag-id')}/${pageIndc++}` + location.search, {},
        function (data, textStatus, jqXHR) {
            $(clicked).next().hide();
            data = JSON.parse(data);
            if (parseInt(data.remPages) <= 0) {
                $(clicked).hide()
            }
            $(clicked).prev().append(data.html);
        },
    );
}

function btnFilterClick() {
    $(this).parent().next('input').val($(this).data('value'));
    let searchObject = {};
    [...$('.filter')].forEach(filter =>
        searchObject[$(filter).find('input').attr('name')] = $(filter).find('input').val()
    );
    filterInSearch(searchObject)

}
function seeMoreAddQue() {
    $(this).next().show();
    let clicked = this;
    $.get(`/similar-questions/${pageIndc++}`,
        {
            'que-title': $('#que-title').val(),
            'category-id': $('#category-id').val(),
            'tags': $('#tags-input').val(),

        },
        function (data, textStatus, jqXHR) {
            $(clicked).next().hide();
            data = JSON.parse(data);
            if (parseInt(data.remPages) <= 0) {
                $(clicked).hide()
            }
            $(clicked).prev().append(data.html);
        },
    );

}
function seeMoreTags() {
    $(this).next().show();
    let clicked = this;
    $.get(`/see-more-tags/${pageIndc++}`,
        {
            'questions': $('#que-filter').val(),
            'answers': $('#ans-filter').val(),
            'category': $('#category-id').val(),

        },
        function (data, textStatus, jqXHR) {
            $(clicked).next().hide();
            data = JSON.parse(data);
            if (parseInt(data.remPages) <= 0) {
                $(clicked).hide()
            }
            $(clicked).prev().append(data.html);
            $(clicked).prev().find(".btn.tag-star").off('click');
            $(clicked).prev().find(".btn.tag-star").click(togTagToFav);
}
        ,
    );

}

function queTitleChange() {
    if (searchText == $(this).val())
        return;
    searchText = $(this).val();


    pageIndc = 0;
    if ($(this).val()) {
        $('#similar-ques').css('display', 'block');
        $('.loading-circle:not(.in-search)').show();
        $(this).next().show();
        $('.questions-list').html('');
        $.get(`/similar-questions/${pageIndc++}`,
            {
                'que-title': $('#que-title').val(),
                'category-id': $('#category-id').val(),
                'tags': $('#tags-input').val(),

            },
            function (data, textStatus, jqXHR) {
                $('.loading-circle:not(.in-search)').hide();
                data = JSON.parse(data);
                if (parseInt(data.remPages) <= 0) {
                    $('.see-more-btn-add-que').hide()
                }
                $('.see-more-btn-add-que').prev().append(data.html);
                if (!data.html) {
                    // $('#similar-ques').css('display','none');

                }
            },
        );
    } else {
        // $('#similar-ques').css('display','none');

    }
}


function addCommentBtn() {
    let csrf = getCookie('csrftoken');
    let clicked = this;
    if ($(this).prev('input').val())
        $.post("/add-comment", {
            'csrfmiddlewaretoken': csrf,
            'post-id': $(this).data('post-id'),
            'text': $(this).prev('input').val()
        },
            function (data, textStatus, jqXHR) {
                $(clicked).prev('input').val('')
                if ($(clicked).parent().siblings('.comments-list').children().last().find('p').hasClass('all-comment-span'))
                    $(clicked).parent().siblings('.comments-list').children().last().before(data);
                else
                    $(clicked).parent().siblings('.comments-list').append(data);

            },
        );
}


// 

function seeAllComments() {
    let clicked = this;
    let ul = $(clicked).parent().parent();
    $.get("/all-comment", { 'post-id': $(this).data('post-id') },
        function (data, textStatus, jqXHR) {
            ul.html('');
            ul.append(data);
            // $(clicked).hide();
        },
    );
}

function changeSugEditStatus() {
    console.log('t');
    let clicked = this;
    let item = $(this).parentsUntil('.await-item').parent();
    $.post("/moderators/change-suggested-edit", {
        'csrfmiddlewaretoken': getCookie('csrftoken'),
        'edit-id': $(this).data('edit-id'),
        'status': $(this).data('action'),
    },
        function (data, textStatus, jqXHR) {
            console.log(data);
            if (data == 'done') {

                if (!$(clicked).hasClass('no-animate')) {

                    item.addClass('ani-await-item');
                    setTimeout(_ => $(item).remove(), 500);
                }
                else {
                    location.reload();
                }
            }
        },
    );

}


function seeMoreUserQue() {
    $(this).next().show();
    let clicked = this;
    $.get(`/profile/see-more-your-questions/${$(this).data('user-id')}/${pageIndc++}`,
        {
            'views': $('#views-inp').val(),
            'votes': $('#votes-inp').val(),
            'answers': $('#answers-inp').val(),
            'search': $('#search-inp').val()
        },
        function (data, textStatus, jqXHR) {
            $(clicked).next().hide();
            data = JSON.parse(data);
            if (parseInt(data.remPages) <= 0) {
                $(clicked).hide()
            }
            $(clicked).prev().append(data.html);
        },
    );


}
function searchUsrQuestions() {
    if (searchText == $(this).val())
        return;
    searchText = $(this).val();

    pageIndc = 0;
    $('.loading-circle:not(.in-search)').show();
    $('.questions-list').html('');
    $.get(`/profile/see-more-your-questions/${$(this).data('user-id')}/${pageIndc++}`,
        {
            'views': $('#views-inp').val(),
            'votes': $('#votes-inp').val(),
            'answers': $('#answers-inp').val(),
            'search': $('#search-inp').val()
        },
        function (data, textStatus, jqXHR) {
            $('.loading-circle:not(.in-search)').hide();
            data = JSON.parse(data);
            if (parseInt(data.remPages) <= 0) {
                $('.see-more-btn-user-que').hide()
            }
            $('.questions-list').append(data.html);
        },
    );

}


function seeMoreUserAns() {
    $(this).next().show();
    let clicked = this;
    $.get(`/profile/see-more-your-answers/${$(this).data('user-id')}/${pageIndc++}`,
        {
            'views': $('#views-inp').val(),
            'votes': $('#votes-inp').val(),
            'answers': $('#answers-inp').val(),
            'search': $('#search-inp').val()
        },
        function (data, textStatus, jqXHR) {
            $(clicked).next().hide();
            data = JSON.parse(data);
            if (parseInt(data.remPages) <= 0) {
                $(clicked).hide()
            }
            $(clicked).prev().append(data.html);
        },
    );


}
function searchUsrAnswers() {
    if (searchText == $(this).val())
        return;
    searchText = $(this).val();
    pageIndc = 0;
    $('.loading-circle:not(.in-search)').show();
    $('.questions-list').html('');
    $.get(`/profile/see-more-your-answers/${$(this).data('user-id')}/${pageIndc++}`,
        {
            'views': $('#views-inp').val(),
            'votes': $('#votes-inp').val(),
            'answers': $('#answers-inp').val(),
            'search': $('#search-inp').val()
        },
        function (data, textStatus, jqXHR) {
            $('.loading-circle:not(.in-search)').hide();
            data = JSON.parse(data);
            if (parseInt(data.remPages) <= 0) {
                $('.see-more-btn-user-que').hide()
            }
            $('.questions-list').append(data.html);
        },
    );

}

function togTagToFav(e) {
    console.log('l');
    let tagId = $(this).data('tag-id');
    let clicked = this;
    function f() {
        let csrf = getCookie('csrftoken');
        $.post("/tog-tag", {
            'csrfmiddlewaretoken': csrf,
            'tag-id': tagId
        },
            function (data, textStatus, jqXHR) {
                if (data == 'added')
                    $(clicked).addClass('favorited');
                else if (data == 'removed')
                    $(clicked).removeClass('favorited');
            },
        );
    }

    checkAuth(f);


}

function checkAuth(fun) {
    $.get({
        url: "/check-auth",
        data: {},
        success(data, textStatus, jqXHR) {
            if (data === '1') {
                fun();
            } else {
                let loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
                loginModal.show();
            }
        },
        // async:false
    }
    );


}
function showCommentDiv() {
    if ($(this).nextAll(".add-comment-div").css("display") == "none")
        checkAuth(_ => $(this).nextAll(".add-comment-div").css("display", "block"));
    else
        $(this).nextAll(".add-comment-div").css("display", "none")
}

function favQueBtn() {
    let clicked = this;
    let f = _ => $.post("/tog-fav-que",
        {
            'que-id': $(this).data('que-id'),
            csrfmiddlewaretoken: getCookie('csrftoken')
        },
        function (data, textStatus, jqXHR) {
            if (data == 'added'){
                $(clicked).addClass('faved-que');
                $(clicked).next('.bookmark-span').addClass('faved-que');
                const v = parseInt($(clicked).next('.bookmark-span').text())+1;
                $(clicked).next('.bookmark-span').text(v);
            }
            else if (data == 'removed'){
                $(clicked).removeClass('faved-que');
                $(clicked).next('.bookmark-span').removeClass('faved-que');
                const v = parseInt($(clicked).next('.bookmark-span').text())-1;
                $(clicked).next('.bookmark-span').text(v);
               }
    },
    );
    checkAuth(f);
}
function folloUserQueBtn() {
    let clicked = this;
    let f = _ => $.post("/togg-user-flo",
        {
            'user-id': $(this).data('user-id'),
            csrfmiddlewaretoken: getCookie('csrftoken')
        },
        function (data, textStatus, jqXHR) {
            if (data == 'added')
                if ($(clicked).hasClass('follow-btn'))
                  $(clicked).html(`<i class="fas fa-user-minus"></i> ${gettext('Unfollow')}`);
                    
                else

                    $(clicked).text(gettext('Unfollow'));
            else if (data == 'removed')
                if ($(clicked).hasClass('follow-btn'))
                    $(clicked).html(`<i class="fas fa-user-plus"></i> ${gettext('Follow')}`);
                else
                    $(clicked).text(gettext('Follow'));
        },
    );
    checkAuth(f);
}


function seeMoreUserBadges() {
    $(this).next().show();
    let page=parseInt($(this).data('page'));
    $(this).data('page',(page+1).toString())
    let clicked = this;
    $.get(`/profile/see-more-badges/${page}`,
        {
            'user-id': $(this).data('user-id'),
            'level': $(this).data('level'),
        },
        function (data, textStatus, jqXHR) {
            $(clicked).next().hide();
            data = JSON.parse(data);
            if (parseInt(data.remPages) <= 0) {
                $(clicked).hide()
            }
            $(clicked).prev().append(data.html);
        },
    );


}

function seeMoreUserFollowers() {
    $(this).next().show();
    let clicked = this;
    $.get(`/profile/see-more-followers/${pageIndc++}`,
        {
            'user-id': $(this).data('user-id'),
        },
        function (data, textStatus, jqXHR) {
            $(clicked).next().hide();
            data = JSON.parse(data);
            if (parseInt(data.remPages) <= 0) {
                $(clicked).hide()
            }
            
            $(clicked).prev().append(data.html);
            $(clicked).prev().find('.follow-btn').off('click');
            $(clicked).prev().find('.follow-btn').click(folloUserQueBtn);
        
        },
    );


}

function seeMoreFavQuestions() {
    $(this).next().show();
    let clicked = this;
    
    $.get(`/profile/see-more-fav-que/${pageIndc++}` , {
            'user-id': $(this).data('user-id'),
            'category': $('#category-id').val(),
            'views': $('#views-filter').val(),
            'votes': $('#votes-filter').val(),
            'answers': $('#answers-filter').val(),
           },
        function (data, textStatus, jqXHR) {
            $(clicked).next().hide();
            data = JSON.parse(data);
            if (parseInt(data.remPages) <= 0) {
                $(clicked).hide()
            }
            $(clicked).prev().append(data.html);
        },
    );
}

function  reportBtnClick(){
    $(`#${$(this).data('type')}-reportModal #report-on`).val($(this).data('report-on'));
}

function searchNavDown(e) {
    if(e.which==40){
        if ($('.search-resaults .active').length==0)
            $('.search-resaults ').children().first().addClass('active')
        else{
            $('.search-resaults .active').next().addClass('active');
            $('.search-resaults .active').first().removeClass('active');
        }
    }

    
    else if(e.which==38){
        if ($('.search-resaults .active').length==0)
            $('.search-resaults ').children().last().addClass('active')
        else{
            $('.search-resaults .active').prev().addClass('active');
            $('.search-resaults .active').last().removeClass('active');
        }
    }
    else if (e.which==13){
        let href=$('.search-resaults .active a').attr('href');
        if(href)
        location.href=href;
        $('.search-nav-form .search-resaults').hide();

    }
 
}
function searchNavUp(e) {
    if(searchText==$(this).val()){
        return;
    }
    searchText=$(this).val();
    if(!$(this).val()){
        $('.search-nav-form .search-resaults').hide();
        $('.search-nav-form .search-resaults').html('');
        
    }
    else{
        $('.search-nav-form .search-resaults').hide();
        $('.search-nav-form .search-resaults').html('');
        $('.loading-circle.in-search').show();
        $.get("/search-que-ajax", {search:searchText},
            function (data, textStatus, jqXHR) {
                $('.loading-circle.in-search').hide();
                if(data){
                    $('.search-nav-form .search-resaults').append(data);
                    $('.search-nav-form .search-resaults li').click(navSearchLiClick);
                    $('.search-nav-form .search-resaults').show();
                    

                    
                }
            },
        );
    }
}



function navSearchLiClick(){
    let href=$(this).find('a').attr('href');
    location.href=href;
    $('.search-nav-form .search-resaults').hide();

}

function checkPollAnswers(){
    let valid=true;
    [...$('.poll-item')].forEach(el=>{
        let inpV=false;
        [...$(el).find('input')].forEach(inp=>{
            if($(inp).is(':checked'))
                inpV=true;
       
        });
        valid=inpV;
    });
    if  (!valid)
        $('.error-poll').slideDown()
    return valid;
}

function submitPoll(){
    
    if(checkPollAnswers())
    $('#poll-form').submit();
}

function customCheckInput(){
    let inp=$(this).prev('input');
    if (inp.is(':checked')){
        inp.removeAttr('checked');
    }
    else{
        inp.attr('checked',true);
    }
}
var oldNumTxt=1;
function numInpDown(e){
    

    if (e.which==38){
        $(this).val(parseInt($(this).val())+1)
        e.preventDefault();
        this.setSelectionRange($(this).val().length,$(this).val().length);
    }
    if (e.which==40){
        $(this).val($(this).val()>1?parseInt($(this).val())-1:1)
        e.preventDefault();
        this.setSelectionRange($(this).val().length,$(this).val().length);
    }
}




(function($) {
    $.fn.inputFilter = function(inputFilter) {
      return this.on("input keydown keyup mousedown mouseup select contextmenu drop", function() {
        if (inputFilter(this.value)) {
          this.oldValue = this.value;
          this.oldSelectionStart = this.selectionStart;
          this.oldSelectionEnd = this.selectionEnd;
        } else if (this.hasOwnProperty("oldValue")) {
          this.value = this.oldValue;
          this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
        } else {
          this.value = "";
        }
      });
    };
  }(jQuery));

function sharePop(){
    let target=$(this).data('target');
    $(target).css('display','block');
    console.log('t');
    if(!$(target).hasClass('showed'))
    setTimeout(()=>$(target).addClass('showed'),100);
    const tooltip = $(target)[0];

    Popper.createPopper(this, tooltip, {
    placement: 'bottom',
    });
}

function copyLink(){ 
    var text = $(this).prev().val();
    navigator.clipboard.writeText(text);
    $(this).addClass('animeted');
    let clicked=this;
    setTimeout(()=>$(clicked).removeClass('animeted'),365);
}