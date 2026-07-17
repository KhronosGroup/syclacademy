// Shared reveal.js setup for SYCL Academy lessons.
//
// A lesson loads reveal.js and its plugins with plain <script> tags (so the
// slides also work when opened directly from the file system), then includes
// this script last:
//
//   <script src="../../js/revealjs/reveal.js"></script>
//   <script src="../../js/revealjs/plugin/markdown.js"></script>
//   <script src="../../js/revealjs/plugin/highlight.js"></script>
//   <script src="../../js/revealjs/plugin/notes.js"></script>
//   <script src="../../js/setup.js"></script>
//
// This file removes the per-lesson duplication of the shared slide styling,
// the global images and the Reveal.initialize call. The core stylesheets are
// plain <link>s in each lesson's <head> so they load render-blocking.

(function () {
  // Paths are resolved relative to the lesson HTML (Lesson_Materials/<name>/index.html).
  var ROOT = "../..";
  var STATIC = ROOT + "/Static";

  // The reveal/theme/custom/highlight stylesheets are plain <link>s in the
  // lesson's <head> so they load render-blocking (no flash of unstyled text).
  // Only the print stylesheet is injected here, since which one is used depends
  // on the ?print-pdf query string.
  var printLink = document.createElement("link");
  printLink.rel = "stylesheet";
  printLink.href = window.location.search.match(/print-pdf/gi)
    ? STATIC + "/css/print/pdf.css"
    : STATIC + "/css/print/paper.css";
  document.head.appendChild(printLink);

  // Shared slide styling that used to be inlined in every lesson.
  var style = document.createElement("style");
  style.textContent =
    ".reveal section pre code { font-size: 0.7em !important; }" +
    " mark { background-color: lightblue; }";
  document.head.appendChild(style);

  // Global images shown on every slide (injected so lessons don't repeat markup).
  function injectGlobalImages() {
    var slides = document.querySelector(".reveal .slides");
    if (!slides || document.getElementById("global-images")) return;

    var container = document.createElement("div");
    container.id = "global-images";
    container.className = "global-images";
    container.innerHTML =
      '<img src="' +
      STATIC +
      '/images/sycl_academy.png" />' +
      '<img src="' +
      STATIC +
      '/images/sycl_logo.png" />' +
      '<div class="trademarks">SYCL and the SYCL logo are trademarks of the Khronos Group Inc.</div>';
    slides.insertBefore(container, slides.firstChild);
  }

  // After reveal builds the slide backgrounds, copy the global images onto each.
  function distributeGlobalImages() {
    var slides = document.getElementsByClassName("slide-background");
    if (slides.length === 0) {
      slides = document.getElementsByClassName("pdf-page");
    }

    var source = document.getElementById("global-images");
    if (!source) return;

    for (var i = 0, max = slides.length; i < max; i++) {
      var cln = source.cloneNode(true);
      cln.removeAttribute("id");
      slides[i].appendChild(cln);
    }

    source.parentElement.removeChild(source);
  }

  injectGlobalImages();

  function initReveal() {
    // Plugins register themselves as globals when their UMD scripts load.
    Reveal.addEventListener("ready", distributeGlobalImages);
    Reveal.initialize({
      plugins: [RevealMarkdown, RevealHighlight, RevealNotes],
      slideNumber: true,
      highlight: {
        beforeHighlight: function (hljs) {
          hljs.addPlugin(mergeHTMLPlugin);
        },
      },
    });
  }

  // Load the merge-html plugin (exposes global `mergeHTMLPlugin`), then init.
  var merge = document.createElement("script");
  merge.src = "../../js/revealjs/plugin/merge-html.js";
  merge.onload = initReveal;
  document.head.appendChild(merge);
})();
