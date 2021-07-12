from aqt import mw
from aqt.utils import showInfo
from anki.hooks import addHook
import anki
import os
import shutil
from .HTMLandCSS import HTMLforEditor, front, back, front_cloze, back_cloze, css

MODEL_NAME = 'KaTeX and Markdown'
CONF_NAME = 'MDKATEX'


def markdownPreview(editor):
    if editor.note.model()["name"] in [MODEL_NAME + " Basic", MODEL_NAME + " Cloze"]:
        editor.web.eval(HTMLforEditor)
        editor.web.eval("""
            var style = document.createElement('style');
            style.type = 'text/css';
            style.innerText = `
                table, th, td {
                    border: 1px solid black;
                    border-collapse: collapse;
                }
                pre code {
                    background-color: #eee;
                    border: 1px solid #999;
                    display: block;
                    padding: 20px;
                    overflow: auto;
                }`;
            document.head.appendChild(style);
        """)
    else:
        editor.web.eval("""
					var area = document.getElementById('markdown-area');
					if(area) area.remove();
        """)


addHook("loadNote", markdownPreview)


def create_model_if_necessacy():
    model = mw.col.models.byName(MODEL_NAME + " Basic")
    model_cloze = mw.col.models.byName(MODEL_NAME + " Cloze")
    m = mw.col.models

    if not model:
        create_model()
    if not model_cloze:
        create_model_cloze()

    update()


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


def update():
    model = mw.col.models.byName(MODEL_NAME + " Basic")
    model_cloze = mw.col.models.byName(MODEL_NAME + " Cloze")

    model['tmpls'][0]['qfmt'] = front
    model['tmpls'][0]['afmt'] = back
    model['css'] = css

    model_cloze['tmpls'][0]['qfmt'] = front_cloze
    model_cloze['tmpls'][0]['afmt'] = back_cloze
    model_cloze['css'] = css

    mw.col.models.save(model)
    mw.col.models.save(model_cloze)

    if os.path.isdir(os.path.join(mw.col.media.dir(), "_katex")):
        shutil.rmtree(os.path.join(mw.col.media.dir(), "_katex"))

    if os.path.isdir(os.path.join(mw.col.media.dir(), "_markdown-it")):
        shutil.rmtree(os.path.join(mw.col.media.dir(), "_markdown-it"))

    addon_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))

    _add_file(os.path.join(addon_path, "_katex.min.js"), "_katex.min.js")
    _add_file(os.path.join(addon_path, "_katex.css"), "_katex.css")
    _add_file(os.path.join(addon_path, "_auto-render.js"), "_auto-render.js")
    _add_file(os.path.join(addon_path, "_markdown-it.min.js"),
              "_markdown-it.min.js")
    _add_file(os.path.join(addon_path, "_highlight.css"), "_highlight.css")
    _add_file(os.path.join(addon_path, "_highlight.js"), "_highlight.js")
    _add_file(os.path.join(addon_path, "_mhchem.js"), "_mhchem.js")

    for katex_font in os.listdir(os.path.join(addon_path, "fonts")):
        _add_file(os.path.join(addon_path, "fonts", katex_font), katex_font)


def _add_file(path, filename):
    if not os.path.isfile(os.path.join(mw.col.media.dir(), filename)):
        mw.col.media.add_file(path)


addHook("profileLoaded", create_model_if_necessacy)
