$(function(){
	var myPostNextPage = $('#my-post-page').prop('value');
	var myPostHasNext = $('#my-post-has-next').prop('value');
	var myFavtNextPage = $('#my-fav-page').prop('value');
	var myFavHasNext = $('#my-fav-has-next').prop('value');
	var followerPostNextPage = $('#follower-post-page').prop('value');
	var followerPostHasNext = $('#follower-post-has-next').prop('value');
	var allPostNextPage = $('#all-post-page').prop('value');
	var allPostHasNext = $('#all-post-has-next').prop('value');
	var otherPostNextPage = $('#other-post-page').prop('value');
	var otherPostHasNext = $('#other-post-has-next').prop('value');
	var otherFavtNextPage = $('#other-fav-page').prop('value');
	var otherFavHasNext = $('#other-fav-has-next').prop('value');
	var followNextPage = $('#follow-page').prop('value');
	var followHasNext = $('#follow-has-next').prop('value');
	var followerNextPage = $('#follower-page').prop('value');
	var followerHasNext = $('#follower-has-next').prop('value');
	var allUserName = 'all'
	var userName = $('.card-subtitle').prop('id');
	var myUserName = $('#my-username').prop('value');

	//お気に入りボタン制御
	$(document).on('submit','.favolite-form',function(event) {
		var postId = $(this).children("input").val();
		event.preventDefault();
		$('#favolite-btn-' + postId).toggleClass('active');
		$('#fav-favolite-btn-' + postId).toggleClass('active');
		$('#all-favolite-btn-' + postId).toggleClass('active');

		//お気に入り登録
		if($('#favolite-btn-' + postId).hasClass('active') || $('#fav-favolite-btn-' + postId).hasClass('active')
				|| $('#all-favolite-btn-' + postId).hasClass('active')){
			$.ajax({
			'url': '../favorite_add/',
            'type': 'POST',
            'data':$(this).serialize(),
            'dataType': 'json',
            'success':function(response){
            	if(response.status == '200'){
        			$('#favolite-off-' + postId).hide();
        			$('#favolite-on-' + postId).show();
        			$('#all-favolite-off-' + postId).hide();
        			$('#all-favolite-on-' + postId).show();
        			$('#fav-favolite-off-' + postId).hide();
        			$('#fav-favolite-on-' + postId).show();
            	}
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
	        			$('#favolite-off-' + postId).show();
	        			$('#favolite-on-' + postId).hide();
	        			$('#myfav-favolite-off-' + postId).show();
	        			$('#myfav-favolite-on-' + postId).hide();
	        			$('#all-favolite-off-' + postId).show();
	        			$('#all-favolite-on-' + postId).hide();
	        			$('#fav-favolite-off-' + postId).show();
	        			$('#fav-favolite-on-' + postId).hide();
	            	}
	            },
			});
		}
	});

	//投稿削除
	$(document).on('submit','.delete-form',function(event) {
		var postId = $(this).children("input").val();
		event.preventDefault();
		var result = confirm('投稿を削除しますか？');
		if(result){
			$.ajax({
				'url': '../post_delete/',
		        'type': 'POST',
		        'data':$(this).serialize(),
		        'dataType': 'json',
		        'success':function(response){
		        	if(response.status == '200'){
		        		window.location.reload();
		        	}
		        },
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
		        		url: '../post_load/?page=' + myPostNextPage + '&username=' + userName,
		        		dataType: 'json',
		        		success: function(response){
		        			response.user_post_list.forEach(function(post){
		        				var content = post.content.replace(/\r\n/g, '\n');
		        				content = content.replace(/\r/g, '\n');
		        				var contentLines = content.split('\n');
		        				var replacedContent = contentLines.join('<br />');
		        				var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
		        				var nextPost = '<li class="list-group-item">';
		        				nextPost += '<span class="font-weight-bold h6"><a href="../home">' + post.user.name + '</a></span>';
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
		        				nextPost += '<input type="hidden" name="csrfmiddlewaretoken" value=' + csrfToken + '>';
		        				nextPost += '</form>';
		        				nextPost += '<form class="delete-form">';
		        				nextPost += '<input type="hidden" name="post_id" value=' + post.post_id + '>';
		        				nextPost += '<button type="submit" class="btn btn-outline-danger btn-sm" >投稿を削除</button>';
		        				nextPost += '<input type="hidden" name="csrfmiddlewaretoken" value=' + csrfToken + '>';
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
		        		url: '../fav_load/?page=' + myFavtNextPage + '&username=' + userName,
		        		dataType: 'json',
		        		success: function(response){
		        			response.user_favorite_list.forEach(function(post){
		        				var content = post.post_content.content.replace(/\r\n/g, '\n');
		        				content = content.replace(/\r/g, '\n');
		        				var contentLines = content.split('\n');
		        				var replacedContent = contentLines.join('<br />');
		        				var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
		        				var nextPost = '<li class="list-group-item">';
		        				if(post.post_content.user.username == userName){
			        				nextPost += '<span class="font-weight-bold h6"><a href="../home">' + post.post_content.user.name + '</a></span>';
		        				}else{
		        					nextPost += '<span class="font-weight-bold h6"><a href=' + '../other_user?username=' + post.post_content.user.username +'>' + post.post_content.user.name + '</a></span>';
		        				}
		        				nextPost += '<p>' + replacedContent + '</p>';
		        				nextPost += '<form class="favolite-form" id=' + 'myfav-' +  post.post_content.post_id + '>';
		        				nextPost += '<input type="hidden" name="post_id" value=' + post.post_content.post_id + '>';
			        		    nextPost += '<button type="submit" class="btn rounded-circle p-0 favolite-btn active" \
			        					style="width:2rem;height:2rem;background:#f0f8ff;" onfocus="this.blur();"\
			        					id=' + 'fav-favolite-btn-' + post.post_content.post_id + '>';
		        				nextPost += '<i class="far fa-star favolite-off" style="display: none;" id=' + 'fav-favolite-off-' + post.post_content.post_id + '></i>';
		        				nextPost += '<i class="fas fa-star favolite-on" id=' + 'fav-favolite-on-' + post.post_content.post_id + '></i>';
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
		//フォロー中の投稿一覧の場合
		if($('#follow-timeline').hasClass('active')){
			var end = document.getElementById('follower-post-end');
			// 表示領域の下端の位置
		    var bottom = this.scrollTop + this.clientHeight;
		    // 末尾の要素の上端の位置
		    var top = end.offsetTop -this.offsetTop;
		    if(followerPostHasNext){
		    //表示している投稿一覧の最下層までスクロールしたら次の投稿一覧をリクエスト
				if (top <= bottom) {
		        	$.ajax({
		        		url: '../post_load/?page=' + followerPostNextPage + '&username=' + userName + '&follow=true',
		        		dataType: 'json',
		        		success: function(response){
		        			response.user_post_list.forEach(function(post){
		        				var content = post.content.replace(/\r\n/g, '\n');
		        				content = content.replace(/\r/g, '\n');
		        				var contentLines = content.split('\n');
		        				var replacedContent = contentLines.join('<br />');
		        				var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
		        				var nextPost = '<li class="list-group-item">';
		        				nextPost += '<span class="font-weight-bold h6"><a href=' + '../other_user?username=' + post.user.username +'>' + post.user.name + '</a></span>';
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
		        				$('#follower-post-list').append(nextPost);
		        			});
		        			followerPostNextPage++;
		        			followerPostHasNext = response.has_next;
		        		}
		        	});
		        }
		    }
		}
		//すべての場合
		if($('#all-timeline').hasClass('active')){
			var end = document.getElementById('all-post-end');
			// 表示領域の下端の位置
		    var bottom = this.scrollTop + this.clientHeight;
		    // 末尾の要素の上端の位置
		    var top = end.offsetTop -this.offsetTop;
		    if(allPostHasNext){
		    //表示している投稿一覧の最下層までスクロールしたら次の投稿一覧をリクエスト
				if (top <= bottom) {
		        	$.ajax({
		        		url: '../post_load/?page=' + allPostNextPage + '&username=' + allUserName,
		        		dataType: 'json',
		        		success: function(response){
		        			response.user_post_list.forEach(function(post){
		        				var favFlg = 0;
		        				var content = post.content.replace(/\r\n/g, '\n');
		        				content = content.replace(/\r/g, '\n');
		        				var contentLines = content.split('\n');
		        				var replacedContent = contentLines.join('<br />');
		        				var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
		        				var nextPost = '<li class="list-group-item">';
		        				if(post.user.username == userName){
			        				nextPost += '<span class="font-weight-bold h6"><a href="../home">' + post.user.name + '</a></span>';
		        				}else{
		        					nextPost += '<span class="font-weight-bold h6"><a href=' + '../other_user?username=' + post.user.username +'>' + post.user.name + '</a></span>';
		        				}
		        				nextPost += '<p>' + replacedContent + '</p>';
		        				nextPost += '<form class="favolite-form" id=' + 'mypos-' +  post.post_id + '>';
		        				nextPost += '<input type="hidden" name="post_id" value=' + post.post_id + '>';
		        				if(post.prefetch_favorite.length == 1){
			        				nextPost += '<button type="submit" class="btn rounded-circle p-0 favolite-btn active" \
			        					style="width:2rem;height:2rem;background:#f0f8ff;" onfocus="this.blur();"\
			        					id=' + 'all-favolite-btn-' + post.post_id + '>';
		        					nextPost += '<i class="far fa-star favolite-off" style="display: none;" id=' + 'all-favolite-off-' + post.post_id + '></i>';
		        					nextPost += '<i class="fas fa-star favolite-on" id=' + 'all-favolite-on-' + post.post_id + '></i>';
		        				}else{
			        				nextPost += '<button type="submit" class="btn rounded-circle p-0 favolite-btn" \
			        					style="width:2rem;height:2rem;background:#f0f8ff;" onfocus="this.blur();"\
			        					id=' + 'all-favolite-btn-' + post.post_id + '>';
		        					nextPost += '<i class="far fa-star favolite-off" id=' + 'all-favolite-off-' + post.post_id + '></i>';
		        					nextPost += '<i class="fas fa-star favolite-on" style="display: none;" id=' + 'all-favolite-on-' + post.post_id + '></i>';
		        				}
		        				nextPost += ' </button>';
		        				nextPost += '<input type="hidden" name="csrfmiddlewaretoken" value=' + csrfToken + '>'
		        				nextPost += '</form>';
		        				if(post.user.username == userName){
			        				nextPost += '<form class="delete-form">';
			        				nextPost += '<input type="hidden" name="post_id" value=' + post.post_id + '>';
			        				nextPost += '<button type="submit" class="btn btn-outline-danger btn-sm" >投稿を削除</button>';
			        				nextPost += '<input type="hidden" name="csrfmiddlewaretoken" value=' + csrfToken + '>';
			        				nextPost += '</form>';
		        				}
		        				nextPost += ' </li>';
		        				$('#all-post-list').append(nextPost);
		        			});
		        			allPostNextPage++;
		        			allPostHasNext = response.has_next;
		        		}
		        	});
		        }
		    }
		}
		//その他ユーザー投稿一覧
		if($('#other-post').hasClass('active')){
			var end = document.getElementById('other-post-end');
			// 表示領域の下端の位置
		    var bottom = this.scrollTop + this.clientHeight;
		    // 末尾の要素の上端の位置
		    var top = end.offsetTop -this.offsetTop;

		    if(otherPostHasNext){
		    //表示している投稿一覧の最下層までスクロールしたら次の投稿一覧をリクエスト
				if (top <= bottom) {
		        	$.ajax({
		        		url: '../post_load/?page=' + otherPostNextPage + '&username=' + userName + '&other=true',
		        		dataType: 'json',
		        		success: function(response){
		        			response.user_post_list.forEach(function(post){
		        				var content = post.content.replace(/\r\n/g, '\n');
		        				content = content.replace(/\r/g, '\n');
		        				var contentLines = content.split('\n');
		        				var replacedContent = contentLines.join('<br />');
		        				var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
		        				var nextPost = '<li class="list-group-item">';
		        				nextPost += '<span class="font-weight-bold h6"><a href=' + '../other_user?username=' + post.user.username +'>' + post.user.name + '</a></span>';
		        				nextPost += '<p>' + replacedContent + '</p>';
		        				nextPost += '<form class="favolite-form" id=' + 'mypos-' +  post.post_id + '>';
		        				nextPost += '<input type="hidden" name="post_id" value=' + post.post_id + '>';
		        				if(Object.keys(post.prefetch_favorite).length){
			        				nextPost += '<button type="submit" class="btn rounded-circle p-0 favolite-btn active" \
			        					style="width:2rem;height:2rem;background:#f0f8ff;" onfocus="this.blur();"\
			        					id=' + 'favolite-btn-' + post.post_id + '>';
		        					nextPost += '<i class="far fa-star favolite-off" style="display: none;" id=' + 'favolite-off-' + post.post_id + '></i>';
		        					nextPost += '<i class="fas fa-star favolite-on" id=' + 'favolite-on-' + post.post_id + '></i>';
		        				}else{
			        				nextPost += '<button type="submit" class="btn rounded-circle p-0 favolite-btn" \
			        					style="width:2rem;height:2rem;background:#f0f8ff;" onfocus="this.blur();"\
			        					id=' + 'favolite-btn-' + post.post_id + '>';
		        					nextPost += '<i class="far fa-star favolite-off" id=' + 'favolite-off-' + post.post_id + '></i>';
		        					nextPost += '<i class="fas fa-star favolite-on" style="display: none;" id=' + 'favolite-on-' + post.post_id + '></i>';
		        				}
		        				nextPost += ' </button>';
		        				nextPost += '<input type="hidden" name="csrfmiddlewaretoken" value=' + csrfToken + '>'
		        				nextPost += '</form>';
		        				nextPost += ' </li>';
		        				$('#other-post-list').append(nextPost);
		        			});
		        			otherPostNextPage++;
		        			otherPostHasNext = response.has_next;
		        		}
		        	});
		        }
		    }
		}
		//その他ユーザー画面のお気に入り一覧の場合
		if($('#other-favorite').hasClass('active')){
			var end = document.getElementById('other-fav-end');
			// 表示領域の下端の位置
		    var bottom = this.scrollTop + this.clientHeight;
		    // 末尾の要素の上端の位置
		    var top = end.offsetTop -this.offsetTop;

		    if(otherFavHasNext){
		    //表示している投稿一覧の最下層までスクロールしたら次の投稿一覧をリクエスト
				if (top <= bottom) {
		        	$.ajax({
		        		url: '../fav_load/?page=' + otherFavtNextPage + '&username=' + userName + '&other=true',
		        		dataType: 'json',
		        		success: function(response){
		        			response.user_favorite_list.forEach(function(post){
		        				var favFlg = 0;
		        				var content = post.post_content.content.replace(/\r\n/g, '\n');
		        				content = content.replace(/\r/g, '\n');
		        				var contentLines = content.split('\n');
		        				var replacedContent = contentLines.join('<br />');

		        				var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
		        				var nextPost = '<li class="list-group-item">';
		        				if(post.post_content.user.username == myUserName){
			        				nextPost += '<span class="font-weight-bold h6"><a href="../home">' + post.post_content.user.name + '</a></span>';
		        				}else{
		        					nextPost += '<span class="font-weight-bold h6"><a href=' + '../other_user?username=' + post.post_content.user.username +'>' + post.post_content.user.name + '</a></span>';
		        				}
		        				nextPost += '<p>' + replacedContent + '</p>';
		        				nextPost += '<form class="favolite-form" id=' + 'myfav-' +  post.post_content.post_id + '>';
		        				nextPost += '<input type="hidden" name="post_id" value=' + post.post_content.post_id + '>';
		        				response.login_user_favorite_list.forEach(function(loginFav){
			        					if( loginFav.post_content != null && loginFav.post_content.post_id == post.post_content.post_id){
			        						favFlg = 1;
			        					}
		        				});
		        				if(favFlg == 1){
				        		    nextPost += '<button type="submit" class="btn rounded-circle p-0 favolite-btn active" \
				        					style="width:2rem;height:2rem;background:#f0f8ff;" onfocus="this.blur();"\
				        					id=' + 'fav-favolite-btn-' + post.post_content.post_id + '>';
			        				nextPost += '<i class="far fa-star favolite-off" style="display: none;" id=' + 'fav-favolite-off-' + post.post_content.post_id + '></i>';
			        				nextPost += '<i class="fas fa-star favolite-on" id=' + 'fav-favolite-on-' + post.post_content.post_id + '></i>';
			        				nextPost += ' </button>';
		        				}else{
				        		    nextPost += '<button type="submit" class="btn rounded-circle p-0 favolite-btn" \
			        					style="width:2rem;height:2rem;background:#f0f8ff;" onfocus="this.blur();"\
			        					id=' + 'favolite-btn-' + post.post_content.post_id + '>';
				        		    nextPost += '<i class="far fa-star favolite-off" id=' + 'fav-favolite-off-' + post.post_content.post_id + '></i>';
				        		    nextPost += '<i class="fas fa-star favolite-on" style="display: none;" id=' + 'fav-favolite-on-' + post.post_content.post_id + '></i>';
				        		    nextPost += ' </button>';
		        				}
		        				nextPost += '<input type="hidden" name="csrfmiddlewaretoken" value=' + csrfToken + '>'
		        				nextPost += '</form>';
		        				nextPost += ' </li>';
		        				$('#other-fav-list').append(nextPost);
		        			});
		        			otherFavtNextPage++;
		        			otherFavHasNext = response.has_next;
		        		}
		        	});
		        }
		    }
		}
		//フォロー中一覧
		if($('#follow').hasClass('active')){
			var end = document.getElementById('follow-end');
			// 表示領域の下端の位置
		    var bottom = this.scrollTop + this.clientHeight;
		    // 末尾の要素の上端の位置
		    var top = end.offsetTop -this.offsetTop;

		    if(followHasNext){
		    //表示している投稿一覧の最下層までスクロールしたら次の投稿一覧をリクエスト
				if (top <= bottom) {
		        	$.ajax({
		        		url: '../follow_follower_load/?page=' + followNextPage + '&username=' + userName,
		        		dataType: 'json',
		        		success: function(response){
		        			response.follow_follower_list.forEach(function(follow){
		        				var nextFollow = '<li class="list-group-item">';
		        				if(follow.followed_user.username == userName){
		        					nextFollow += '<span class="font-weight-bold h6"><a href="../home">' +follow.followed_user.name + '</a></span>';
		        				}else{
		        					nextFollow += '<span class="font-weight-bold h6"><a href=' + '../other_user?username=' + follow.followed_user.username +'>' + follow.followed_user.name + '</a></span>';
		        				}
		        				nextFollow += '<div class="text-muted mb-2">' + follow.followed_user.username + '</div>';
		        				nextFollow += ' </li>';
		        				$('#follow-list').append(nextFollow);
		        			});
		        			followNextPage++;
		        			followHasNext = response.has_next;
		        		}
		        	});
		        }
		    }
		}
		//フォロワー一覧
		if($('#follower').hasClass('active')){
			var end = document.getElementById('follower-end');
			// 表示領域の下端の位置
		    var bottom = this.scrollTop + this.clientHeight;
		    // 末尾の要素の上端の位置
		    var top = end.offsetTop -this.offsetTop;

		    if(followerHasNext){
		    //表示している投稿一覧の最下層までスクロールしたら次の投稿一覧をリクエスト
				if (top <= bottom) {
		        	$.ajax({
		        		url: '../follow_follower_load/?page=' + followerNextPage + '&username=' + userName + '&follower=True',
		        		dataType: 'json',
		        		success: function(response){
		        			response.follow_follower_list.forEach(function(follower){
		        				var nextFollow = '<li class="list-group-item">';
		        				if(follower.follow_user.username == userName){
		        					nextFollow += '<span class="font-weight-bold h6"><a href="../home">' +follower.follow_user.name + '</a></span>';
		        				}else{
		        					nextFollow += '<span class="font-weight-bold h6"><a href=' + '../other_user?username=' + follower.follow_user.username +'>' + follower.follow_user.name + '</a></span>';
		        				}
		        				nextFollow += '<div class="text-muted mb-2">' + follower.follow_user.username + '</div>';
		        				nextFollow += ' </li>';
		        				$('#follower-list').append(nextFollow);
		        			});
		        			followerNextPage++;
		        			followerHasNext = response.has_next;
		        		}
		        	});
		        }
		    }
		}
	});
});