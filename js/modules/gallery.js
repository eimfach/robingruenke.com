(function GalleryModule(){
  document.querySelectorAll('.gallery-background').forEach(function(topEl){
    var mainImage = topEl.querySelector('.main-image');

      topEl.querySelectorAll('.gallery-picture').forEach(function(img){

        img.onclick = function() {
          var imgSrc = img.getAttribute('src')
          var mainImageSrc = mainImage.getAttribute('src')
          
          img.setAttribute('src', mainImageSrc)
          mainImage.setAttribute('src', imgSrc)
        }
      });

  });
})();