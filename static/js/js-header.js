$(document).ready(function () {

	
	
	$('.film-podb__item').each(function () {
		if( $(this).index() >= 24 ){
			$(this).hide()
		}
	})
	
	$('.films__li').each(function () {
		if( $(this).index() >= 2 ){
			$(this).hide()
		}
	})

})