$(document).on('click','.btn_prev',function(event){
    loadItems($(event.target).attr('value'), 'prev', $(event.target), $(event.target).closest('div').parent());
});
$(document).on('click','.btn_next',function(event){
    loadItems($(event.target).attr('value'), 'next', $(event.target), $(event.target).closest('div').parent());
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
                html.push('<div>');
                if(!paragraph.is_parallelfirst)
                    html.push('<a class="btn_prev" value="',paragraph.id, '" index="', paragraph.index ,'">prev</a>');
                html.push('<button name="prev_p" type="submit" value="',paragraph.id,'">new branch</button>');
                if(!paragraph.is_parallellast)
                    html.push('<a class="btn_next" value="',paragraph.id,'" index="',paragraph.index,'">next</a>');                html.push('<p>',paragraph.text,'</p>');
            });
            console.log(html.join(""));
            var it = pwt.closest('div').parentElement;
            pwt.closest('div').remove();
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
