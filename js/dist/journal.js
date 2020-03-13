// auto generated, don't modify 

document.addEventListener("DOMContentLoaded", function(event) {

// https://github.com/javan/form-request-submit-polyfill/blob/master/form-request-submit-polyfill.js
(function RequestSubmitPolyfillModule(prototype) {
  if (typeof prototype.requestSubmit == "function") return

  prototype.requestSubmit = function(submitter) {
    if (submitter) {
      validateSubmitter(submitter, this)
      submitter.click()
    } else {
      submitter = document.createElement("input")
      submitter.type = "submit"
      submitter.hidden = true
      this.appendChild(submitter)
      submitter.click()
      this.removeChild(submitter)
    }
  }

  function validateSubmitter(submitter, form) {
    submitter instanceof HTMLElement || raise(TypeError, "parameter 1 is not of type 'HTMLElement'")
    submitter.type == "submit" || raise(TypeError, "The specified element is not a submit button")
    submitter.form == form || raise(DOMException, "The specified element is not owned by this form element", "NotFoundError")
  }

  function raise(errorConstructor, message, name) {
    throw new errorConstructor("Failed to execute 'requestSubmit' on 'HTMLFormElement': " + message + ".", name)
  }
})(HTMLFormElement.prototype);

// https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent/CustomEvent
(function CustomEventPolyfillModule() {

  if ( typeof window.CustomEvent === "function" ) return false;

  function CustomEvent ( event, params ) {
    params = params || { bubbles: false, cancelable: false, detail: null };
    var evt = document.createEvent( 'CustomEvent' );
    evt.initCustomEvent( event, params.bubbles, params.cancelable, params.detail );
    return evt;
   }

  window.CustomEvent = CustomEvent;
})();

// Source: https://gist.github.com/k-gun/c2ea7c49edf7b757fe9561ba37cb19ca
/**
 * Element.prototype.classList for IE8/9, Safari.
 * @author    Kerem Güneş <k-gun@mail.com>
 * @copyright Released under the MIT License <https://opensource.org/licenses/MIT>
 * @version   1.2
 * @see       https://developer.mozilla.org/en-US/docs/Web/API/Element/classList
 */
;(function ClassListPolyfillModule() {
  // Helpers.
  var trim = function(s) {
          return s.replace(/^\s+|\s+$/g, '');
      },
      regExp = function(name) {
          return new RegExp('(^|\\s+)'+ name +'(\\s+|$)');
      },
      forEach = function(list, fn, scope) {
          for (var i = 0; i < list.length; i++) {
              fn.call(scope, list[i]);
          }
      };

  // Class list object with basic methods.
  function ClassList(element) {
      this.element = element;
  }

  ClassList.prototype = {
      add: function() {
          forEach(arguments, function(name) {
              if (!this.contains(name)) {
                  this.element.className = trim(this.element.className +' '+ name);
              }
          }, this);
      },
      remove: function() {
          forEach(arguments, function(name) {
              this.element.className = trim(this.element.className.replace(regExp(name), ' '));
          }, this);
      },
      toggle: function(name) {
          return this.contains(name) ? (this.remove(name), false) : (this.add(name), true);
      },
      contains: function(name) {
          return regExp(name).test(this.element.className);
      },
      item: function(i) {
          return this.element.className.split(/\s+/)[i] || null;
      },
      // bonus
      replace: function(oldName, newName) {
          this.remove(oldName), this.add(newName);
      }
  };

  // IE8/9, Safari
  // Remove this if statements to override native classList.
  if (!('classList' in Element.prototype)) {
  // Use this if statement to override native classList that does not have for example replace() method.
  // See browser compatibility: https://developer.mozilla.org/en-US/docs/Web/API/Element/classList#Browser_compatibility.
  // if (!('classList' in Element.prototype) ||
  //     !('classList' in Element.prototype && Element.prototype.classList.replace)) {
      Object.defineProperty(Element.prototype, 'classList', {
          get: function() {
              return new ClassList(this);
          }
      });
  }

  // For others replace() support.
  if (window.DOMTokenList && !DOMTokenList.prototype.replace) {
      DOMTokenList.prototype.replace = ClassList.prototype.replace;
  }
})();

(function StartUpModule(){
  document.body.className = "grayscale"
})();

(function ChapterIndexModule(){
  var chapterIndexToggle = document.getElementById('chapter-index-toggle')
  var chapterIndexList = document.getElementById('chapter-index-list')
  if (chapterIndexToggle && chapterIndexList) {
    chapterIndexToggle.onclick = function(){
      if (getComputedStyle(chapterIndexList).getPropertyValue("display") === "none") {
        chapterIndexToggle.style = 'text-align: left'
        chapterIndexList.style = 'display: block'
      } else {
        chapterIndexList.style = 'display: none'
        chapterIndexToggle.style = 'text-align: center'
      }
       
    }
  }

})();

(function ArticleUpdateHintModule(){
  if(window.localStorage) {
    var pageTitle = document.getElementById('pagetitle').textContent.trim().split(' ').join('-').toLowerCase()
    var key = pageTitle + '-article-count'
    var lastChapterCount = localStorage.getItem(key)

    if(!lastChapterCount) {
      localStorage.setItem(key, countChapters())
    } else {
      var updatedChapterCount = countChapters()

      if (updatedChapterCount > lastChapterCount) {
        // enable blockquote highlight
        var highlightEl = document.getElementById('new-chapter-hint')

        if (highlightEl) {
          
          var firstNewChapterEl = document.querySelectorAll('.chapter')[lastChapterCount]
          var firstNewChapterElId = firstNewChapterEl.getAttribute('id')

          highlightEl.setAttribute('href', '#' + firstNewChapterElId)
          
          highlightEl.style = 'display: block'

          localStorage.setItem(key, updatedChapterCount)
        }
        
      }
    }
  }

  function countChapters() {
    var chapterCount = 0

    document.querySelectorAll('.chapter').forEach(function(el) {
      chapterCount = chapterCount + 1
    });

    return chapterCount
  }
})();

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

(function FeedbackModule(){
  document.querySelectorAll('.leave-feedback').forEach(function(feedbackEl){
    feedbackEl.onclick = function(){
      var idFragment = feedbackEl.getAttribute('id').split('feedback-toggle-')[1]
      var formContainer = document.getElementById('feedback-form-container-' + idFragment)
      if (getComputedStyle(formContainer).getPropertyValue('display') == 'none'){
        formContainer.style = 'display: block'
        textarea = formContainer.querySelector('textarea')
        textarea.focus()
      } else {
        formContainer.style = 'display: none'
      }
    }
  });
})();

(function LikeSubmitModule(){
  var featureContainer = document.getElementById('feature-like-journal')

  if (featureContainer) {
    var likeform = featureContainer.querySelector('#like-form')
    var submitIcon = likeform.querySelector('.submit')

    submitIcon.onclick = function(){
      // HTMLFormElement.prototype.requestSubmit helps with applying a form submit event emitter on any element besides button and input
      // It does trigger a submit event (HTMLFormElement.prototype.submit does not)
      likeform.requestSubmit()
    }

    if (typeof window.fetch === 'function') {
      likeform.onsubmit = function(e){
        e.preventDefault()

        submitIcon.onclick = null
        submitIcon.classList.remove('icon-bubble-love-streamline-talk')
        submitIcon.classList.remove('font-big')
        submitIcon.textContent = 'Thanks :)'

        formData = {
          method: likeform.method,
          headers: {
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
          },
          body: new URLSearchParams(new FormData(likeform)).toString()
        }
        // send the form
        fetch('/', formData)
          .catch(function(resp, a){
            var interval = null
            var retries = 0

            interval = setInterval(function() {
              if (retries === 10) {
                clearInterval(interval)
              } else {
                retries = retries + 1
                fetch('/', formData)
                  .then(function(){
                    clearInterval(interval)
                  })
              }
            }, 7500)
          })
        
      }
    }
  }

})();




});