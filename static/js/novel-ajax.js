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
                    html.push('<a class="btn_prev" value="',paragraph.id, '" index="', paragraph.index ,'"><&nbsp<&nbsp<&nbsp&nbsp&nbsp</a>');
                    else {
                    html.push('<a class="hollow"></a>');
                    }
                html.push('<p class="mainstory">',paragraph.text,'</p>');
                if(!paragraph.is_parallellast)
                    html.push('<a class="btn_next" value="',paragraph.id,'" index="',paragraph.index,'">&nbsp&nbsp&nbsp>&nbsp>&nbsp></a>');
                    else {
                    html.push('<a class="hollow"></a>');
                    }
                html.push('</div>');
                html.push('<button name="prev_p" class="newbranch" type="submit" value="',paragraph.id,'">Create branch</button>');
            });
            console.log(html.join(""));
            var it = pwt.closest('div').parentElement;
            pwt.closest('div').parent().remove();
            $("<div>" + html.join("")+"</div>").appendTo(par);

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
        html.push('<div>');
        if(paragraph[3] == "False")
            html.push('<a class="btn_prev" value="',paragraph[1], '" index="', paragraph[2] ,'">prev</a>');
        html.push('<button name="prev_p" type="submit" value="',paragraph[1],'">new branch</button>');
        if(paragraph[4] == "False")
            html.push('<a class="btn_next" value="',paragraph[1],'" index="',paragraph[2],'">next</a>');
        html.push('<p>',paragraph[0],'</p>');
    });
    $("<div>" + html.join("")+"</div>").appendTo($('#novelbox'));

});
