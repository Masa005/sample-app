$(function(){
	var nextPage = $('.page').prop('value');
	var hasNext = $('.has-next').prop('value');

	//お気に入りボタン制御
	$('.favolite-btn').on('click', function(event){
		event.preventDefault();
		$(this).toggleClass('active');
		if($(this).hasClass('active')){
			$('.favolite-off').hide();
			$('.favolite-on').show();
		} else {
			$('.favolite-off').show();
			$('.favolite-on').hide();
		}
	});

	//無限スクロール
	$('.tab-content').on('scroll',function() {
		var end = document.getElementById('end');
		// 表示領域の下端の位置
	    var bottom = this.scrollTop + this.clientHeight;
	    // 末尾の要素の上端の位置
	    var top = end.offsetTop -this.offsetTop;

	    if(hasNext){
	    //表示している投稿一覧の最下層までスクロールしたら次の投稿一覧をリクエスト
			if (top <= bottom) {
	        	$.ajax({
	        		url: '../post_load/?page=' + nextPage,
	        		dataType: 'json',
	        		success: function(response){
	        			response.user_post_list.forEach(function(post ){

	        				var content = post.content.replace(/\r\n/g, '\n');
	        				content = content.replace(/\r/g, '\n');
	        				var contentLines = content.split('\n');
	        				var replacedContent = contentLines.join('<br />');

	        				var nextPost = '<li class="list-group-item">';
	        				nextPost += '<span class="font-weight-bold h6">' + post.user.name + '</span>';
	        				nextPost += '<p>' + replacedContent + '</p>';
	        				nextPost += '<bunextPoston type="bunextPoston" class="btn rounded-circle p-0 favolite-btn" \
	        					style="width:2rem;height:2rem;background:#f0f8ff;" onfocus="this.blur();"\
	        					id="favolite-btn">';
	        				nextPost += '<i class="far fa-star favolite-off" id="favolite-off"></i>';
	        				nextPost += '<i class="fas fa-star favolite-on" style="display: none;" id="favolite-on"></i>';
	        				nextPost += ' </bunextPoston>';
	        				nextPost += ' </li>';
	        				$('.list-group').append(nextPost);
	        			});
	        			nextPage++;
        				hasNext = response.has_next;
	        		}
	        	});
	        }
	    }
	});
});