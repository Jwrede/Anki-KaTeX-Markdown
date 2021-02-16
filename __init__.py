from aqt import mw
from anki.hooks import addHook
import anki

MODEL_NAME = "KaTeX and Markdown"


def create_model_if_necessacy():
    model = mw.col.models.byName(MODEL_NAME + " Basic")
    model_cloze = mw.col.models.byName(MODEL_NAME + " Cloze")

    if not model:
        create_model()
    if not model_cloze:
        create_model_cloze()


def create_model():
    m = mw.col.models
    model = m.new(MODEL_NAME + " Basic")

    field = m.newField("Front")
    m.addField(model, field)

    field = m.newField("Back")
    m.addField(model, field)

    template = m.newTemplate(MODEL_NAME + " Basic")
    template['qfmt'] = front
    template['afmt'] = back
    model['css'] = css

    m.addTemplate(model, template)
    m.add(model)
    m.save(model)


def create_model_cloze():
    m = mw.col.models
    model = m.new(MODEL_NAME + " Cloze")
    model["type"] = anki.consts.MODEL_CLOZE

    field = m.newField("Text")
    m.addField(model, field)

    field = m.newField("Back Extra")
    m.addField(model, field)

    template = m.newTemplate(MODEL_NAME + " Cloze")
    template['qfmt'] = front_cloze
    template['afmt'] = back_cloze
    model['css'] = css

    m.addTemplate(model, template)
    m.add(model)
    m.save(model)


addHook("profileLoaded", create_model_if_necessacy)


front = """
<div id="front">{{Front}}</div>

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css" integrity="sha384-AfEj0r4/OFrOo5t7NnNe46zW/tFgW6x/bCJG8FqQCEo3+Aro6EYUG4+cU+KJWu/X" crossorigin="anonymous">
<script>
	let katex = document.createElement('script');
	katex.onload = function() {
		let katex_auto_loader = document.createElement('script');
		katex_auto_loader.onload = function() {
			let markdownIt = document.createElement('script');
			markdownIt.onload = function() {
				renderMath("front");
				markdown("front");
			}
			markdownIt.src = "https://cdnjs.cloudflare.com/ajax/libs/markdown-it/12.0.4/markdown-it.min.js";
			document.head.appendChild(markdownIt);
		}
		katex_auto_loader.src = "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/contrib/auto-render.min.js";
		document.head.appendChild(katex_auto_loader);
	}
	katex.src = "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js";
	document.head.appendChild(katex);

	function renderMath(ID) {
		let text = document.getElementById(ID).innerHTML;
		text = replaceInString(text);
		document.getElementById(ID).innerHTML = text;
		renderMathInElement(document.getElementById(ID), {
			delimiters:  [
  				{left: "$$", right: "$$", display: true},
  				{left: "$", right: "$", display: false}
			],
		});
	}
	function markdown(ID) {
		let md = new markdownit({typographer: true, html:true});
		let text = document.getElementById(ID).innerHTML;
		document.getElementById(ID).innerHTML = md.render(text);
	}
	function replaceInString(str) {
		str = str.replace(/<br\s*[\/]?>/gi, "\\n");
		str = str.replace(/&nbsp;/g, " ");
		str = str.replace(/<div>/g, "\\n");
		return str.replace(/<\/div>/g, "\\n");
	}
</script>
"""

back = """
<div id="front">{{Front}}</div>

<hr id=answer>

<div id="back">{{Back}}</div>

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css" integrity="sha384-AfEj0r4/OFrOo5t7NnNe46zW/tFgW6x/bCJG8FqQCEo3+Aro6EYUG4+cU+KJWu/X" crossorigin="anonymous">
<script>
	let katex = document.createElement('script');
	katex.onload = function() {
		let katex_auto_loader = document.createElement('script');
		katex_auto_loader.onload = function() {
			let markdownIt = document.createElement('script');
			markdownIt.onload = function() {
				renderMath("front");
				markdown("front");
				renderMath("back");
				markdown("back");
			}
			markdownIt.src = "https://cdnjs.cloudflare.com/ajax/libs/markdown-it/12.0.4/markdown-it.min.js";
			document.head.appendChild(markdownIt);
		}
		katex_auto_loader.src = "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/contrib/auto-render.min.js";
		document.head.appendChild(katex_auto_loader);
	}
	katex.src = "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js";
	document.head.appendChild(katex);

	function renderMath(ID) {
		let text = document.getElementById(ID).innerHTML;
		text = replaceInString(text);
		document.getElementById(ID).innerHTML = text;
		renderMathInElement(document.getElementById(ID), {
			delimiters:  [
  				{left: "$$", right: "$$", display: true},
  				{left: "$", right: "$", display: false}
			],
		});
	}
	function markdown(ID) {
		let md = new markdownit({typographer: true, html:true});
		let text = document.getElementById(ID).innerHTML;
		document.getElementById(ID).innerHTML = md.render(text);
	}
	function replaceInString(str) {
		str = str.replace(/<br\s*[\/]?>/gi, "\\n");
		str = str.replace(/&nbsp;/g, " ");
		str = str.replace(/<div>/g, "\\n");
		return str.replace(/<\/div>/g, "\\n");
	}
</script>
"""

front_cloze = """
<div id="front">{{cloze:Text}}</div>

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css" integrity="sha384-AfEj0r4/OFrOo5t7NnNe46zW/tFgW6x/bCJG8FqQCEo3+Aro6EYUG4+cU+KJWu/X" crossorigin="anonymous">
<script>
	let katex = document.createElement('script');
	katex.onload = function() {
		let katex_auto_loader = document.createElement('script');
		katex_auto_loader.onload = function() {
			let markdownIt = document.createElement('script');
			markdownIt.onload = function() {
				renderMath("front");
				markdown("front");
			}
			markdownIt.src = "https://cdnjs.cloudflare.com/ajax/libs/markdown-it/12.0.4/markdown-it.min.js";
			document.head.appendChild(markdownIt);
		}
		katex_auto_loader.src = "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/contrib/auto-render.min.js";
		document.head.appendChild(katex_auto_loader);
	}
	katex.src = "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js";
	document.head.appendChild(katex);

	function renderMath(ID) {
		let text = document.getElementById(ID).innerHTML;
		text = replaceInString(text);
		document.getElementById(ID).innerHTML = text;
		renderMathInElement(document.getElementById(ID), {
			delimiters:  [
  				{left: "$$", right: "$$", display: true},
  				{left: "$", right: "$", display: false}
			],
		});
	}
	function markdown(ID) {
		let md = new markdownit({typographer: true, html:true});
		let text = document.getElementById(ID).innerHTML;
		document.getElementById(ID).innerHTML = md.render(text);
	}
	function replaceInString(str) {
		str = str.replace(/<br\s*[\/]?>/gi, "\\n");
		str = str.replace(/&nbsp;/g, " ");
		str = str.replace(/<div>/g, "\\n");
		str = str.replace(/<span[^>]*>/gi, "");
		return str.replace(/<\/div>/g, "\\n");
	}
</script>
"""

back_cloze = """
<div id="back">{{cloze:Text}}</div><br>
<div id="extra">{{Back Extra}}</div>

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css" integrity="sha384-AfEj0r4/OFrOo5t7NnNe46zW/tFgW6x/bCJG8FqQCEo3+Aro6EYUG4+cU+KJWu/X" crossorigin="anonymous">
<script>
	let katex = document.createElement('script');
	katex.onload = function() {
		let katex_auto_loader = document.createElement('script');
		katex_auto_loader.onload = function() {
			let markdownIt = document.createElement('script');
			markdownIt.onload = function() {
				renderMath("back");
				markdown("back");
				renderMath("extra");
				markdown("extra");
			}
			markdownIt.src = "https://cdnjs.cloudflare.com/ajax/libs/markdown-it/12.0.4/markdown-it.min.js";
			document.head.appendChild(markdownIt);
		}
		katex_auto_loader.src = "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/contrib/auto-render.min.js";
		document.head.appendChild(katex_auto_loader);
	}
	katex.src = "https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js";
	document.head.appendChild(katex);

	function renderMath(ID) {
		let text = document.getElementById(ID).innerHTML;
		text = replaceInString(text);
		document.getElementById(ID).innerHTML = text;
		renderMathInElement(document.getElementById(ID), {
			delimiters:  [
  				{left: "$$", right: "$$", display: true},
  				{left: "$", right: "$", display: false}
			],
		});
	}
	function markdown(ID) {
		let md = new markdownit({typographer: true, html:true});
		let text = document.getElementById(ID).innerHTML;
		document.getElementById(ID).innerHTML = md.render(text);
	}
	function replaceInString(str) {
		str = str.replace(/<br\s*[\/]?>/gi, "\\n");
		str = str.replace(/&nbsp;/g, " ");
		str = str.replace(/<div>/g, "\\n");
		str = str.replace(/<span[^>]*>/gi, "");
		return str.replace(/<\/div>/g, "\\n");
	}
</script>
"""

css = """

.card {
  font-family: arial;
  font-size: 20px;
  color: black;
  background-color: white;
}
table, th, td {
	border: 1px solid black;
	border-collapse: collapse;
}
code {
    background: #f4f4f4;
    border: 1px solid #ddd;
    border-left: 3px solid #f36d33;
    color: #666;
    page-break-inside: avoid;
    font-family: monospace;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 1.6em;
    max-width: 100%;
    overflow: auto;
    padding: 1em 1.5em;
    display: block;
    word-wrap: break-word;
}
"""
