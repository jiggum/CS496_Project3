$(document).on('click','#imagetotext',function(event){
    loadItems($("#itt").val());
});

var loadItems = function(img_url) {

    var url = "http://143.248.48.228:8124/notecalc?imgpath="+img_url + "&rotate=0&lang=eng";
	window.open(url);
};

