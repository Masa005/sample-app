$(function(){
	var leapYearFlg = false
	var month30 = ["4","6","9","11"];
	var february = ["29","30","31"];
	var leapFebruary = ["30","31"];
	//「年」選択時、閏年の判別を行う
	$('#id_birthday_year').on('change',function(){
		if($(this).val() % 4 == 0 && ($(this).val() % 100 != 0 || $(this).val() % 400 == 0)){
			leapYearFlg = true;
			if($('#id_birthday_month').val() == "2"){
				$('#id_birthday_day').find('option').each(function(){
					var value = $(this).val();
					var wrap = $(this).parents().attr("class");
					if(value == "29"){
						 if(wrap == "wrap"){
							  $(this).unwrap();
						    }
					}
				});
			}
		}else{
			leapYearFlg = false
			if($('#id_birthday_month').val() == "2"){
				$('#id_birthday_day').find('option').each(function(){
					var value = $(this).val();
					var wrap = $(this).parents().attr("class");
					if(value == "29"){
						 if(wrap !== "wrap"){
							 $(this).wrap("<span class='wrap'>");
						    }
					}
				});
			}
		}
	});
	//「月」選択時、選択した「月」によって「日」の項目を変更
	$('#id_birthday_month').on('change',function(){
		if(month30.includes($(this).val())){
			$('#id_birthday_day').find('option').each(function(){
				var value = $(this).val();
				var wrap = $(this).parents().attr("class");
				if(value == "31"){
					 if(wrap !== "wrap"){
					      $(this).wrap("<span class='wrap'>");
					    }
				}
			});
		} else 	if($(this).val() == "2"){
			if(leapYearFlg){
				$('#id_birthday_day').find('option').each(function(){
					var value = $(this).val();
					var wrap = $(this).parents().attr("class");
					if(leapFebruary.includes($(this).val())){
						 if(wrap !== "wrap"){
						      $(this).wrap("<span class='wrap'>");
						    }
					}
				});
			} else {
				$('#id_birthday_day').find('option').each(function(){
					var value = $(this).val();
					var wrap = $(this).parents().attr("class");
					if(february.includes($(this).val())){
						 if(wrap !== "wrap"){
						      $(this).wrap("<span class='wrap'>");
						    }
					}
				});
			}
		} else {
			$('#id_birthday_day').find('option').each(function(){
				var value = $(this).val();
				var wrap = $(this).parents().attr("class");
				if(february.includes($(this).val())){
					if(wrap == "wrap"){
					      $(this).unwrap();
					    }
				}
			});
		}
	});
});