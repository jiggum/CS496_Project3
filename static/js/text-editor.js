function replaceSelectionWithHtml(tag) {
	var range, html, temp, temp_node, base, exit=false;
	range = window.getSelection().getRangeAt(0);
	temp = range.toString();
	base = window.getSelection().baseNode.parentNode;
	base_parent = base.parentNode
		while(base.tagName != "DIV" && base.tagName != "SPAN"){
			$(base).contents().unwrap();
			if(base.tagName == "H2" || base.tagName == "B"|| base.tagName == "I"|| base.tagName == "BLOCKQUOTE"){
                temp = base.textContent;
				exit = true;
				break;
			}

			temp_node = base_parent;
			base_parent = base.parentNode;
			base = temp_node;
		};
	var div = document.createElement("div");
	if(exit){
        base.deleteContents();
		div.innerHTML = temp;
	}
	else{
	    range.deleteContents();
        if(temp.length>0)
    		div.innerHTML = "<" + tag + ">" + temp + "</" + tag + ">";
        else
            div.innerHTML = temp;
	}
	var frag = document.createDocumentFragment(), child;
	while ( (child = div.firstChild) ) {
		frag.appendChild(child);
	}
	range.insertNode(frag);
}
$(document).on('click','#subtitle',function(){
	replaceSelectionWithHtml("h2");
});
$(document).on('click','#bold',function(){
	replaceSelectionWithHtml("b");
});
$(document).on('click','#italic',function(){
	replaceSelectionWithHtml("i");
});
$(document).on('click','#quote',function(){
	replaceSelectionWithHtml("blockquote");
});

$(document).on('click','#submit',function(){
	var text_str = $('#novel_text').contents();
	var text_temp = "";
	for(i=0;i<text_str .length;i++){
		if(text_str [i].outerHTML === undefined){
			text_temp+=text_str[i].textContent;
		}
		else{
			text_temp+=text_str[i].outerHTML;
		}
	}
	$('#text').val(text_temp);
	$('#hidden_submit').click()
});

