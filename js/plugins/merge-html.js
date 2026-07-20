// highlight.js mergeHTMLPlugin: preserves author HTML (e.g. <mark>) in
// data-noescape code blocks. Exposes global `mergeHTMLPlugin`.

var mergeHTMLPlugin = (function () {
  "use strict";

  var originalStream;

  function escapeHTML(value) {
    return value
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#x27;");
  }

  function tag(node) {
    return node.nodeName.toLowerCase();
  }

  function nodeStream(node) {
    var result = [];
    (function _nodeStream(node, offset) {
      for (var child = node.firstChild; child; child = child.nextSibling) {
        if (child.nodeType === 3) {
          offset += child.nodeValue.length;
        } else if (child.nodeType === 1) {
          result.push({ event: "start", offset: offset, node: child });
          offset = _nodeStream(child, offset);
          if (!tag(child).match(/br|hr|img|input/)) {
            result.push({ event: "stop", offset: offset, node: child });
          }
        }
      }
      return offset;
    })(node, 0);
    return result;
  }

  function mergeStreams(original, highlighted, value) {
    var processed = 0;
    var result = "";
    var nodeStack = [];

    function selectStream() {
      if (!original.length || !highlighted.length) {
        return original.length ? original : highlighted;
      }
      if (original[0].offset !== highlighted[0].offset) {
        return original[0].offset < highlighted[0].offset
          ? original
          : highlighted;
      }
      return highlighted[0].event === "start" ? original : highlighted;
    }

    function open(node) {
      function attributeString(attr) {
        return " " + attr.nodeName + '="' + escapeHTML(attr.value) + '"';
      }
      result +=
        "<" +
        tag(node) +
        [].map.call(node.attributes, attributeString).join("") +
        ">";
    }

    function close(node) {
      result += "</" + tag(node) + ">";
    }

    function render(event) {
      (event.event === "start" ? open : close)(event.node);
    }

    while (original.length || highlighted.length) {
      var stream = selectStream();
      result += escapeHTML(value.substring(processed, stream[0].offset));
      processed = stream[0].offset;
      if (stream === original) {
        nodeStack.reverse().forEach(close);
        do {
          render(stream.splice(0, 1)[0]);
          stream = selectStream();
        } while (
          stream === original &&
          stream.length &&
          stream[0].offset === processed
        );
        nodeStack.reverse().forEach(open);
      } else {
        if (stream[0].event === "start") {
          nodeStack.push(stream[0].node);
        } else {
          nodeStack.pop();
        }
        render(stream.splice(0, 1)[0]);
      }
    }
    return result + escapeHTML(value.substr(processed));
  }

  return {
    "before:highlightElement": function (data) {
      originalStream = nodeStream(data.el);
    },
    "after:highlightElement": function (data) {
      if (!originalStream.length) return;
      var resultNode = document.createElement("div");
      resultNode.innerHTML = data.result.value;
      data.result.value = mergeStreams(
        originalStream,
        nodeStream(resultNode),
        data.text
      );
      data.el.innerHTML = data.result.value;
    },
  };
})();
