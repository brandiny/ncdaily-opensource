
var carousel = document.querySelector('.carousel')
var flky = new Flickity( carousel , {
    cellAlign: 'left',
    contain: true,
    wrapAround: true,
    freeScroll: true,
    imagesLoaded: true,
    autoPlay: 5000
});



function spin() {
    for (var i=0; i < 5; i++) {
        flky.next();
    }
    // adding styling
    var carouselcells = document.getElementsByClassName('carousel-cell');
    var carouselcellstext = document.getElementsByClassName('carousel-cell-text');

    for (var i=0; i < carouselcells.length; i++) {
        carouselcells[i].style.padding = '0 1em';
        // carouselcellstext[i].style,padding = '1em 3em';
    }


    document.getElementById('carousel-above').style.color = 'darkgrey';
}

carousel.addEventListener("webkitAnimationEnd", spin);
carousel.addEventListener("animationend", spin);
carousel.addEventListener("oanimationend", spin);