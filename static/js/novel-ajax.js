$(document).on('click','.btn_prev',function(event){
    loadItems($(event.target).attr('value'), 'prev', $(event.target), $(event.target).closest('div').parent().parent());
});
$(document).on('click','.btn_next',function(event){
    loadItems($(event.target).attr('value'), 'next', $(event.target), $(event.target).closest('div').parent().parent());
});

var loadItems = function(ph_id, direction, pwt, par) {

    var url = "/parallelstory/?phid="+ph_id + "&direction=" + direction;
    $.ajax({
        type:"GET",
        url: url,
        success: function(responseData) {
            var data = JSON.parse(responseData);
            var html = [];
            $.each(data.paragraphs, function(index, paragraph){
                html.push('<div style="text-align:center">');
                html.push('<div class="moving">');
                if(!paragraph.is_parallelfirst)
                    html.push('<a class="btn_prev" value="',paragraph.id, '" index="', paragraph.index ,'">《</a>');
                else {
                    html.push('<a class="hollow"></a>');
                }
                html.push('<div class="mainstory">',paragraph.text,'</div>');
                if(!paragraph.is_parallellast)
                    html.push('<a class="btn_next" value="',paragraph.id,'" index="',paragraph.index,'">》</a>');
                else {
                    html.push('<a class="hollow"></a>');
                }
                html.push('</div>');
                html.push('<button name="prev_p" class="newbranch" type="submit" value="',paragraph.id,'">Create Branch</button>');
                html.push('<small><span class="heart fa-stack fa-sm"><i class="fa fa-stack-1x fa-heart-o">',paragraph.like,'</i></span></small>');
            });
            console.log(html.join(""));
            var it = pwt.closest('div').parentElement;
            pwt.closest('div').parent().remove();
            $("<div>" + html.join("")+"</div>").appendTo(par);
            like_check();

        },
        error:function(){
        },
        complete: function(data){
        }
    });
};
$(document).ready(function(){
    var html = [];
    paragraphs = $('.first_text')
    $.each(paragraphs, function(index, paragraph_u){
        paragraph = paragraph_u.value.split("^|&|");
        html.push('<div style="text-align:center">');
        html.push('<div class="moving">');
        if(paragraph[3] == "False")
            html.push('<a class="btn_prev" value="',paragraph[1], '" index="', paragraph[2] ,'">《</a>');
        else {
            html.push('<a class="hollow"></a>');
        }

        html.push('<div class="mainstory">',paragraph[0],'</div>');
        if(paragraph[4] == "False")
            html.push('<a class="btn_next" value="',paragraph[1],'" index="',paragraph[2],'">》</a>');
        else {
            html.push('<a class="hollow"></a>');
        }
        html.push('</div>');
        html.push('<button name="prev_p" class="newbranch" type="submit" value="',paragraph[1],'">Create Branch</button>');
        html.push('<small><span class="heart fa-stack fa-sm"><i class="fa fa-stack-1x fa-heart-o">',paragraph[5],'</i></span></small>');

    });
    $("<div>" + html.join("")+"</div>").appendTo($('#novelbox'));

});


var like = function() {
    var temp = temp = $(".newbranch");
    p_id = temp[temp.length-1].value;
    var url = "/like/?prev_p=" + p_id;
    $.ajax({
        type:"GET",
        url: url,
        success: function(responseData) {
            var s = JSON.parse(responseData).state;
            if(s){
                $("#like_i").removeClass("fa-heart-o").addClass("fa-heart");
            }
            else{
                alert("Already Liked");
            }

        },
        error:function(){
        },
        complete: function(data){
        }
    });
};
var like_check = function() {
    var temp = temp = $(".newbranch");
    p_id = temp[temp.length-1].value;
    var url = "/like_check/?prev_p=" + p_id;
    $.ajax({
        type:"GET",
        url: url,
        success: function(responseData) {
            var s = JSON.parse(responseData).state;
            if(s){
                $("#like_i").removeClass("fa-heart-o").addClass("fa-heart");
            }
            else{
                $("#like_i").removeClass("fa-heart").addClass("fa-heart-o");
            }


        },
        error:function(){
        },
        complete: function(data){
        }
    });
};

$(document).on('click','#like_i',function(event){
    like();
});
$(document).ready(function(){
    like_check();
});
