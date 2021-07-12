$(document).ready(function () {

    $(".category-list-item").click(CategoryListClick);
    $(".categories-list").children().first().click();

    $(".add-cate-m-btn").click(addCateClick);

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
        $(cateLi).text(element['name']);
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
    
    // listToAddId=$(this).parent().next(".categories-list").attr("id");

}
function searchTagTable(){
    
}