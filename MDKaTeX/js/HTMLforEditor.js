var area = document.getElementById('markdown-area');
if (area) area.remove();
area = document.createElement('markdown-area');
area.id = 'markdown-area';
area.style.display = 'inline-block';
area.style.overflowY = 'auto';
area.style.padding = '1%';
area.style.visibility = 'hidden';
area.style.width = '98%';
area.style.height = '100%';

var fields = document.getElementById('fields');
if (fields !== null) {
  keyupFunc = function () {
    var text = '# Field 1\n' + fields.children[0].children[1].shadowRoot.children[2].innerHTML;
    text += "\n# Field 2\n" + fields.children[1].children[1].shadowRoot.children[2].innerHTML;
    render(text);
  }

  document.body.appendChild(area);
}

else {
  var fields = document.getElementsByClassName('fields')[0];

  keyupFunc = function () {
    var text = '# Field 1\n' + fields.children[0].getElementsByClassName("rich-text-editable")[0].shadowRoot.children[2].innerHTML;
    text += "\n# Field 2\n" + fields.children[1].getElementsByClassName("rich-text-editable")[0].shadowRoot.children[2].innerHTML;
    render(text);
  }

  fields.appendChild(area);
}


var getResources = [
  getCSS("style.css", "https://cdn.jsdelivr.net/gh/alexthillen/Anki-KaTeX-Markdown@main/MDKaTeX/css/style.css"),
  getCSS("_katex.css", "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css"),
  getCSS("_highlight.css", "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.0.1/styles/default.min.css"),
  getScript("_highlight.js", "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.0.1/highlight.min.js"),
  getScript("_katex.min.js", "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js"),
  getScript("_auto-render.js", "https://cdn.jsdelivr.net/gh/Jwrede/Anki-KaTeX-Markdown/auto-render-cdn.js"),
  getScript("_markdown-it.min.js", "https://cdnjs.cloudflare.com/ajax/libs/markdown-it/12.0.4/markdown-it.min.js"),
  getScript("_markdown-it-mark.js", "https://cdn.jsdelivr.net/gh/Jwrede/Anki-KaTeX-Markdown/_markdown-it-mark.js")
];

main = function () {
  keyupFunc();
  document.addEventListener('keyup', keyupFunc);
}

Promise.all(getResources).then(() => getScript("_mhchem.js", "https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/contrib/mhchem.min.js")).then(main);


function getScript(path, altURL) {
  return new Promise((resolve, reject) => {
    let script = document.createElement("script");
    script.onload = resolve;
    script.onerror = function () {
      let script_online = document.createElement("script");
      script_online.onload = resolve;
      script_online.onerror = reject;
      script_online.src = altURL;
      document.head.appendChild(script_online);
    }
    script.src = path;
    document.head.appendChild(script);
  })
}

function replaceSpan(str) {
  let tokenized = str.split(/(<span.*?>|<\/span>)/g);
  let isCloze = false;
  tokenized = tokenized.map((element, idx) => {
    if (element.includes("<span class='cloze'>") || element.includes('<span class="cloze">')) {
      isCloze = true;
      return "<span class='cloze'>";
    } else if (isCloze && element.includes("</span>")) {
      isCloze = false;
      return "</span>";
    } else if (element.includes("<span")) {
      return "";
    } else if (element.includes("</span>")) {
      return "";
    } else {
      return element;
    }
  });
  return tokenized.join("");
}

function getCSS(path, altURL) {
  return new Promise((resolve, reject) => {
    var css = document.createElement('link');
    css.setAttribute('rel', 'stylesheet');
    css.type = 'text/css';
    css.onload = resolve;
    css.onerror = function () {
      var css_online = document.createElement('link');
      css_online.setAttribute('rel', 'stylesheet');
      css_online.type = 'text/css';
      css_online.onload = resolve;
      css_online.onerror = reject;
      css_online.href = altURL;
      document.head.appendChild(css_online);
    }
    css.href = path;
    document.head.appendChild(css);
  });
}

function render(text) {
  renderMath(text);
  markdown(text);
  show();
}

function show() {
  area.style.visibility = "visible";
}


function renderMath(text) {
  text = replaceInString(text);
  area.textContent = text;
  renderMathInElement(area, {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "$", right: "$", display: false }
    ],
    throwOnError: false
  });
}
function markdown() {
  let element = area;
  element.innerHTML = element.innerHTML.replaceAll('\\$', '&dollar;');
  let md = new markdownit({
    typographer: true, html: true, highlight: function (str, lang) {
      if (lang && hljs.getLanguage(lang)) {
        try {
          return hljs.highlight(str, { language: lang }).value;
        } catch (__) { }
      }

      return ''; // use external default escaping
    }
  }).use(markdownItMark);
  text = replaceHTMLElementsInString(element.innerHTML);
  text = md.render(text);
  element.innerHTML = text.replace(/&lt;\/span&gt;/gi, "\\");
}
function replaceInString(str) {
  str = str.replace(/<[\/]?pre[^>]*>/gi, "");
  str = str.replace(/<br\s*[\/]?[^>]*>/gi, "\n");
  str = str.replace(/<div[^>]*>/gi, "\n");
  // Thanks Graham A!
  str = replaceSpan(str)
  str = str.replace(/<\/div[^>]*>/g, "\n");
  return replaceHTMLElementsInString(str);
}

function replaceHTMLElementsInString(str) {
  str = str.replace(/&nbsp;/gi, " ");
  str = str.replace(/&tab;/gi, "	");
  str = str.replace(/&gt;/gi, ">");
  str = str.replace(/&lt;/gi, "<");
  return str.replace(/&amp;/gi, "&");
}