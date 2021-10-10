function r(f){/in/.test(document.readyState)?setTimeout('r('+f+')',9):f()}
function asd(){
	r(function(){
	    if (!document.getElementsByClassName) {
	        // Поддержка IE8
	        var getElementsByClassName = function(node, classname) {
	            var a = [];
	            var re = new RegExp('(^| )'+classname+'( |$)');
	            var els = node.getElementsByTagName("*");
	            for(var i=0,j=els.length; i < j; i++)
	                if(re.test(els[i].className))a.push(els[i]);
	            return a;
	        }
	        var videos = getElementsByClassName(document.body,"youtube");
	    } else {
	        var videos = document.getElementsByClassName("youtube");
	    }

	    var nb_videos = videos.length;
	    for (var i=0; i < nb_videos; i++) {
	        // Находим постер для видео, зная ID нашего видео
	        videos[i].style.backgroundImage = 'url(http://i.ytimg.com/vi/' + videos[i].id + '/sddefault.jpg)';

	        // Размещаем над постером кнопку Play, чтобы создать эффект плеера
	        var play = document.createElement("div");
	        play.setAttribute("class","play");
	        videos[i].appendChild(play);

	        videos[i].onclick = function() {
	            // Создаем iFrame и сразу начинаем проигрывать видео, т.е. атрибут autoplay у видео в значении 1
	            var iframe = document.createElement("iframe");
	            var iframe_url = "https://www.youtube.com/embed/" + this.id + "?autoplay=1&autohide=1";
	            if (this.getAttribute("data-params")) iframe_url+='&'+this.getAttribute("data-params");
	            iframe.setAttribute("src",iframe_url);
	            iframe.setAttribute("allow",'autoplay');
	            iframe.setAttribute("mute",'1');
	            iframe.setAttribute("frameborder",'0');

	            // Высота и ширина iFrame будет как у элемента-родителя
	            iframe.style.width  = this.style.width;
	            iframe.style.height = this.style.height;

	            // Заменяем начальное изображение (постер) на iFrame
	            this.parentNode.replaceChild(iframe, this);
	        }
	    }
	});
}

asd();


[].forEach.call(document.querySelectorAll('img[data-src]'),    function(img) {
  img.setAttribute('src', img.getAttribute('data-src'));
  img.onload = function() {
    img.removeAttribute('data-src');
  };
});

// Wow JS

if(document.querySelector('.wow'))
	new WOW().init();

// Wow JS

$(document).ready(function () {


	$('.banner h1').each(function () {
		if( $(this).width() > 1100 ){
			$(this).css('max-width', '100%')
		}
		else{
			$(this).css('max-width', '414px')
		}
	})


	$('.films li').each(function () {
		if( $(this).index() >= 9 ){
			$(this).addClass('li_more')

			$(this).hide()
		}
	})





	
	var iframes = $('iframe')
	var linkYput = ''

	iframes.attr('data-src', function() {
    var src = $(this).parent().attr('src');
    $(this).parent().removeAttr('src');
    return src;
	});

	$('.film-block__item .photo__play').click(function () {
		$(this).parent().parent().find('.popup-film').addClass('popup_open')

		asd();

		iframes.attr('src', function() {
        return $(this).parent().find('iframe').data('src');
    });


    linkYput = $(this).parent().parent().find('.youtube').attr('id')

    $('.slick-slider').addClass('nnn')
	})

	$('.films .li__sides .photo__play').click(function () {
		$(this).parent().parent().find('.popup-film').addClass('popup_open')

		asd();

		iframes.attr('src', function() {
      return $(this).parent().find('iframe').data('src');
    });

		linkYput = $(this).parent().parent().find('.youtube').attr('id')

    $('.slick-slider').addClass('nnn')
	})

	$('.film__trailer .photo__play').click(function () {
		$(this).parent().find('.popup-film').addClass('popup_open')

		asd();

		linkYput = $(this).parent().parent().find('.youtube').attr('id')

		iframes.attr('src', function() {
      return $(this).parent().find('iframe').data('src');
    });


	})

	$('.popup__close, .popup__bgd').click(function () {
		
    
	  $(this).parent().find('iframe').attr("src", $(this).parent().find('iframe').attr("src"));



		// iframes = $(this).parent().find('iframe');

		// $(this).parent().find('.popup__content').html(`<div class="youtube" id="${linkYput}" style="background-image: url(&quot;http://i.ytimg.com/vi/${linkYput}/sddefault.jpg&quot;);"><div class="play"></div></div>`)
		$(this).parent().find('.popup__content').html(`<div class="youtube" id="${linkYput}"></div>`)

    $('.slick-slider').removeClass('nnn')
		$(this).parent().removeClass('popup_open')

		// iframes.attr('src', function() {
  //     return $(this).parent().find('iframe').data('src');
  //   });

		// iframes.attr('data-src', function() {
		//     var src = $(this).parent().attr('src');
		//     $(this).parent().removeAttr('src');
		//     return src;
		// });

		// $(this).parent().find('iframe').attr("src", '');
	})




	$('.film-block__slider').slick({
		slidesToShow: 5,
		swipeToSlide: true,
		infinite: false,
		responsive: [
			{
				breakpoint: 1281,
				settings: {
					slidesToShow: 4,
				}
			},
			{
				breakpoint: 1140,
				settings: {
					slidesToShow: 3,
				}
			},
			{
				breakpoint: 992,
				settings: {
					slidesToShow: 4,
				}
			},
			{
				breakpoint: 768,
				settings: "unslick"
			}
		]
	})

	$('.banner-slider').slick({
		arrows: false,
		dots: true,
		infinite: false,
	})

	$('.slider__block').slick({
		arrows: true,
		dots: true,
		infinite: false,
	})

	$('.header__burger').click(function () {
		$('.header__nav').slideDown()
	})

	$('.header__search_mob').click(function () {
		$('.header__search_menu').slideDown()
	})

	$('.header__burger_close').click(function () {
		$(this).parent().parent().parent().slideUp()
	})


	$('.films .film__description').each(function (e) {
		if( $(this).find('p').height() <= 239 ){
			$(this).find('.more').hide()
		}
	})

	$('.authors__all').click(function () {
		$('.authors__block').css('max-height', '100%')
		$('.authors').css('padding-bottom', '0')

		$(this).hide()
	})

	$('.films .film__description .more').click(function () {
		$(this).parent().find('p').addClass('open')

		$(this).hide()
	})

	if( $(document).width() < 992 ){
		$('.have_child .menu__link').click(function (e) {
			e.preventDefault();

			$(this).parent().find('ul').slideToggle(200)
			$(this).parent().toggleClass('li_open')
		})
	}

	let f = 0 
	let z = 0;
	let itmPodb = 24;
	let itmFilms = 2;
	$(document).scroll(function () {

		let scrollTopDocument = $(document).scrollTop()
		let heightWindow = $(window).height()
		let heightDocument = $(document).height()
		let heightFooter = $('footer').height()

		let heightSum = ((scrollTopDocument + heightWindow)/0.8) - heightDocument + heightFooter

		// Каталог
		// Каталог
		// Каталог
		if( heightSum > 0 && z == 0 && $('.film-podb__item').hasClass('film-podb__item')){
			$('.loading').html('Загрузка...')
			z = 1;

			setTimeout(function () {
				itmPodb = itmPodb + 24;
				$('.film-podb__item').each(function () {
					$(this).show()
					if( $(this).index() >= itmPodb ){
						$(this).hide()
					}
				})
				z = 0
				$('.loading').html('')
				return false;
			}, 1000)
		}
		// Каталог
		// Каталог
		// Каталог





		// Главная
		// Главная
		// Главная
		if( heightSum > 0 && z == 0 && $('.films__li').hasClass('films__li')){
			$('.loading').html('Загрузка...')
			z = 1;

			setTimeout(function () {
				itmFilms = itmFilms + 2;
				$('.films__li').each(function () {
					$(this).show()
					if( $(this).index() >= itmFilms ){
						$(this).hide()
					}
				})
				z = 0
				$('.loading').html('')
				return false;
			}, 1000)
		}// Главная
		// Главная
		// Главная

		$('.films .li__sides').each(function () {
			let offTop = $(this).offset().top
			let thisHeight = $(this).height()
			let docScrollSum = (thisHeight / 1.2) + $(document).scrollTop()
			
			if( offTop < docScrollSum && f == 0 ){
				var circleProgress = (function(selector) {
			    var wrapper = document.querySelectorAll(selector);
			    Array.prototype.forEach.call(wrapper, function(wrapper, i) {
			      var wrapperWidth,
			        wrapperHeight,
			        percent,
			        innerHTML,
			        context,
			        lineWidth,
			        centerX,
			        centerY,
			        radius,
			        newPercent,
			        speed,
			        from,
			        to,
			        duration,
			        start,
			        strokeStyle,
			        text;

			      var getValues = function() {
			        wrapperWidth = parseInt(window.getComputedStyle(wrapper).width);
			        wrapperHeight = wrapperWidth;
			        percent = wrapper.getAttribute('data-cp-percentage');
			        innerHTML = '<span class="percentage"><strong>' + percent + '</strong> %</span><canvas class="circleProgressCanvas" width="' + (wrapperWidth * 2) + '" height="' + wrapperHeight * 2 + '"></canvas>';
			        wrapper.innerHTML = innerHTML;
			        text = wrapper.querySelector(".percentage");
			        canvas = wrapper.querySelector(".circleProgressCanvas");
			        wrapper.style.height = canvas.style.width = canvas.style.height = wrapperWidth + "px";
			        context = canvas.getContext('2d');
			        centerX = canvas.width / 2;
			        centerY = canvas.height / 2;
			        newPercent = 0;
			        speed = 1;
			        from = 0;
			        to = percent;
			        duration = 2000;
			        lineWidth = 9;
			        radius = canvas.width / 2 - lineWidth;
			        strokeStyle = wrapper.getAttribute('data-cp-color');
			        start = new Date().getTime();
			      };

			      function animate() {
			        requestAnimationFrame(animate);
			        var time = new Date().getTime() - start;
			        if (time <= duration) {
			          var x = easeInOutQuart(time, from, to - from, duration);
			          newPercent = x;
			          text.innerHTML = '';
			          drawArc();
			        }
			      }

			      function drawArc() {
			        var circleStart = 1.5 * Math.PI;
			        var circleEnd = circleStart + (newPercent / 50) * Math.PI;
			        context.clearRect(0, 0, canvas.width, canvas.height);
			        context.beginPath();
			        context.arc(centerX, centerY, radius, circleStart, 4 * Math.PI, false);
			        context.lineWidth = lineWidth;
			        context.strokeStyle = "#121415";
			        context.stroke();
			        context.beginPath();
			        context.arc(centerX, centerY, radius, circleStart, circleEnd, false);
			        context.lineWidth = lineWidth;
			        context.strokeStyle = strokeStyle;
			        context.stroke();

			      }
			      var update = function() {
			        getValues();
			        animate();
			      }
			      update();

			      var resizeTimer;
			      window.addEventListener("resize", function() {
			        clearTimeout(resizeTimer);
			        resizeTimer = setTimeout(function() {
			          clearTimeout(resizeTimer);
			          start = new Date().getTime();
			          update();
			        }, 250);
			      });
			    });

			    //
			    // http://easings.net/#easeInOutQuart
			    //  t: current time
			    //  b: beginning value
			    //  c: change in value
			    //  d: duration
			    //
			    function easeInOutQuart(t, b, c, d) {
			      if ((t /= d / 2) < 1) return c / 2 * t * t * t * t + b;
			      return -c / 2 * ((t -= 2) * t * t * t - 2) + b;
			    }

			  });

			  circleProgress('.counter');

			  // Gibt eine Zufallszahl zwischen min (inklusive) und max (exklusive) zurück
			  function getRandom(min, max) {
			    return Math.random() * (max - min) + min;
			  }
			  f = 1


			}

		})

	})

})






























  