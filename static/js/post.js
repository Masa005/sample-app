$(function(){
	var myPostNextPage = $('#my-post-page').prop('value');
	var myPostHasNext = $('#my-post-has-next').prop('value');
	var myFavtNextPage = $('#my-fav-page').prop('value');
	var myFavHasNext = $('#my-fav-has-next').prop('value');
	var userName = $('.card-subtitle').prop('id');
	var prefixNum = 6;

	//お気に入りボタン初期表示
	$(document).ready( function(){
		favInit();
	});

	//お気に入りボタン制御
	$(document).on('submit','.favolite-form',function(event) {

		var tenpPostId = $(this).attr('id');

		var postId = tenpPostId.slice( prefixNum ) ;
		event.preventDefault();
		$('#favolite-btn-' + postId).toggleClass('active');
		//お気に入り登録
		if($('#favolite-btn-' + postId).hasClass('active')){
			$.ajax({
			'url': '../favorite_add/',
            'type': 'POST',
            'data':$(this).serialize(),
            'dataType': 'json',
            'success':function(response){
            	if(response.status == '200'){
            		alert('お気に入り登録しました');
        			$('#favolite-off-' + postId).hide();
        			$('#favolite-on-' + postId).show();
            	}else{
            		alert('お気に入り登録に失敗しました');
            	}
            },
            'error':function(){
        		alert('お気に入り登録に失敗しました');
            },
			});
		} else {
			//お気に入り削除
			$.ajax({
				'url': '../favorite_delete/',
	            'type': 'POST',
	            'data':$(this).serialize(),
	            'dataType': 'json',
	            'success':function(response){
	            	if(response.status == '200'){
	            		alert('お気に入りを削除しました');
	        			$('#favolite-off-' + postId).show();
	        			$('#favolite-on-' + postId).hide();
	        			$('#myfav-favolite-off-' + postId).show();
	        			$('#myfav-favolite-on-' + postId).hide();
	            	}else{
	            		alert('お気に入り削除に失敗しました');
	            	}
	            },
	            'error':function(){
	            	alert('お気に入り削除に失敗しました');
	            }
			});
		}
	});

	//無限スクロール
	$('.tab-content').on('scroll',function() {
		//投稿一覧の場合
		if($('#post').hasClass('active')){
			var end = document.getElementById('my-post-end');
			// 表示領域の下端の位置
		    var bottom = this.scrollTop + this.clientHeight;
		    // 末尾の要素の上端の位置
		    var top = end.offsetTop -this.offsetTop;

		    if(myPostHasNext){
		    //表示している投稿一覧の最下層までスクロールしたら次の投稿一覧をリクエスト
				if (top <= bottom) {
		        	$.ajax({
		        		url: '../post_load/?page=' + myPostNextPage + '&user-name=' + userName,
		        		dataType: 'json',
		        		success: function(response){
		        			response.user_post_list.forEach(function(post){
		        				var content = post.content.replace(/\r\n/g, '\n');
		        				content = content.replace(/\r/g, '\n');
		        				var contentLines = content.split('\n');
		        				var replacedContent = contentLines.join('<br />');
		        				var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
		        				var nextPost = '<li class="list-group-item">';
		        				nextPost += '<span class="font-weight-bold h6">' + post.user.name + '</span>';
		        				nextPost += '<p>' + replacedContent + '</p>';
		        				nextPost += '<form class="favolite-form" id=' + 'mypos-' +  post.post_id + '>';
		        				nextPost += '<input type="hidden" name="post_id" value=' + post.post_id + '>';
		        				if(post.prefetch_favorite.length == 1){
			        				nextPost += '<button type="submit" class="btn rounded-circle p-0 favolite-btn active" \
			        					style="width:2rem;height:2rem;background:#f0f8ff;" onfocus="this.blur();"\
			        					id=' + 'favolite-btn-' + post.post_id + '>';
		        				}else{
			        				nextPost += '<button type="submit" class="btn rounded-circle p-0 favolite-btn" \
			        					style="width:2rem;height:2rem;background:#f0f8ff;" onfocus="this.blur();"\
			        					id=' + 'favolite-btn-' + post.post_id + '>';
		        				}
		        				if(post.prefetch_favorite.length == 1){
		        					nextPost += '<i class="far fa-star favolite-off" style="display: none;" id=' + 'favolite-off-' + post.post_id + '></i>';
		        					nextPost += '<i class="fas fa-star favolite-on" id=' + 'favolite-on-' + post.post_id + '></i>';
		        				}else{
		        					nextPost += '<i class="far fa-star favolite-off" id=' + 'favolite-off-' + post.post_id + '></i>';
		        					nextPost += '<i class="fas fa-star favolite-on" style="display: none;" id=' + 'favolite-on-' + post.post_id + '></i>';
		        				}
		        				nextPost += ' </button>';
		        				nextPost += '<input type="hidden" name="csrfmiddlewaretoken" value=' + csrfToken + '>'
		        				nextPost += '</form>';
		        				nextPost += ' </li>';
		        				$('#my-post-list').append(nextPost);
		        			});
		        			myPostNextPage++;
		        			myPostHasNext = response.has_next;
		        		}
		        	});
		        }
		    }
		}
		//お気に入り一覧の場合
		if($('#favorite').hasClass('active')){
			var end = document.getElementById('my-fav-end');
			// 表示領域の下端の位置
		    var bottom = this.scrollTop + this.clientHeight;
		    // 末尾の要素の上端の位置
		    var top = end.offsetTop -this.offsetTop;

		    if(myFavHasNext){
		    //表示している投稿一覧の最下層までスクロールしたら次の投稿一覧をリクエスト
				if (top <= bottom) {
		        	$.ajax({
		        		url: '../fav_load/?page=' + myFavtNextPage + '&user-name=' + userName,
		        		dataType: 'json',
		        		success: function(response){
		        			response.user_favorite_list.forEach(function(post){
		        				var content = post.post_content.content.replace(/\r\n/g, '\n');
		        				content = content.replace(/\r/g, '\n');
		        				var contentLines = content.split('\n');
		        				var replacedContent = contentLines.join('<br />');
		        				var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
		        				var nextPost = '<li class="list-group-item">';
		        				nextPost += '<span class="font-weight-bold h6">' + post.user.name + '</span>';
		        				nextPost += '<p>' + replacedContent + '</p>';
		        				nextPost += '<form class="favolite-form" id=' + 'myfav-' +  post.post_content.post_id + '>';
		        				nextPost += '<input type="hidden" name="post_id" value=' + post.post_content.post_id + '>';
			        		    nextPost += '<button type="submit" class="btn rounded-circle p-0 favolite-btn active" \
			        					style="width:2rem;height:2rem;background:#f0f8ff;" onfocus="this.blur();"\
			        					id=' + 'favolite-btn-' + post.post_content.post_id + '>';
		        				nextPost += '<i class="far fa-star favolite-off" style="display: none;" id=' + 'favolite-off-' + post.post_content.post_id + '></i>';
		        				nextPost += '<i class="fas fa-star favolite-on" id=' + 'favolite-on-' + post.post_content.post_id + '></i>';
		        				nextPost += ' </button>';
		        				nextPost += '<input type="hidden" name="csrfmiddlewaretoken" value=' + csrfToken + '>'
		        				nextPost += '</form>';
		        				nextPost += ' </li>';
		        				$('#my-fav-list').append(nextPost);
		        			});
		        			myFavtNextPage++;
		        			myFavHasNext = response.has_next;
		        		}
		        	});
		        }
		    }
		}
	});

	function favInit(){
		$(".favolite-form").each(function(i, elem) {
			var tenpPostId = $(this).attr('id');
			var postId = tenpPostId.slice( prefixNum ) ;
			if($('#favolite-btn-' + postId).hasClass('active')){
				$('#favolite-off-' + postId).hide();
				$('#favolite-on-' + postId).show();
			} else {
				$('#favolite-off-' + postId).show();
				$('#favolite-on-' + postId).hide();
			}
		});
	}
});