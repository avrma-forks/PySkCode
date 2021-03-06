# SkCode - BBcode parser implementation for Python 3
## By Fabien Batteix (alias Skywodd) 

### Overview

This project is a pure python BBCode to HTML / text rendering engine.

The code included in this project converts [BBCode](http://en.wikipedia.org/wiki/BBCode) into HTML ready for display, or plain text ready for mailing.

The code is split into three parts:
- the parser / tokenizer / document builder engine,
- the post-parsing related code (aka utilities), 
- the rendering engine.

The code is designed to be modular and easy to extend to match any possible use-case. 

**Starting from version 3, this project is considered production ready and is heavily unit-tested.**

### Installation

Installation is easy as doing ``pip install pygments git+https://github.com/TamiaLab/PySkCode.git``.

Note: on systems like Debian, the ``pip`` command for Python 3.x may have been renamed ``pip3``.

### Requirements

This project require Python 3.4 or later (tested with Python 3.4).

No external dependencies are required, only Python stdlib import are used.

**EDIT:** Code blocks now require [Pygments](http://pygments.org/) for syntax highlighting.

### Basic usage / Quickstart

```python
from skcode import parse_skcode, render_to_html

document = parse_skcode('[h1]Hello World![/h1]')

print(render_to_html(document))
```

### Advantages Over [Postmarkup](https://code.google.com/p/postmarkup/) or [dcwatson/bbcode](https://github.com/dcwatson/bbcode)

- Powerful tag lexer with escape sequences support in quoted attribute value, also support unquoted value and self closing tags.
- No regular expressions for low-level parsing, only pure (and readable) Python code.
- Per tag options with easy subclassing possible, give you the power to choose how any tag should work, even internal one.
- Class based implementation, a tag is nothing more than a single class. No callable and nested dict nightmare.
- Nothing hard-coded, you can choose how any stage of the code should work with your application.
- Made to be extensible and clean, no horrible monolithic spaghetti monster like other BBCode parser.
- DOM-like parser, you can post-process the document tree and add your own sauce if necessary.
- Useful toolkit of post-parsing utilities included, like auto-paragraph utility, summary extractor and more.
- Sanitation of nested tag included out-the-box on per tag rules basis. **work in progress**
- Error message support built-in, can be disabled at rendering, really useful for "preview mode".
- Smileys and cosmetics replacement support, with some classic default rules per default.
- User-proof settings by default. Import and play.
- Can generate HTML, text (real text version, not a html-striped version) or both, you choose.
- HTML and CSS made to work out-the-box with Bootstrap 3 and Font-Awesome 4.

### Implemented BBCode tags and syntax

The ``DEFAULT_RECOGNIZED_TAGS`` setting include the following tag definitions.

N.B. Some tags included by default require CSS to work. 
If you're using Bootstrap 3 and Font-Awesome 4 for your CSS, you're already ready to go.

#### Acronyms / Abbreviations

Tag name: ``abbr`` (alias: ``acronym``)

Supported attribute: ``title`` (alias: tag name)

Syntax: ``Do this [abbr title="As Soon As Possible"]ASAP[/abbr].``

Shortcut syntax: ``Do this [abbr="As Soon As Possible"]ASAP[/abbr].``

#### Alert box
 
Tag name: ``alert`` (alias: see below)

Supported attributes: ``title`` (alias: tag name), ``type`` (see below)

Syntax: ``[alert title="Shit happen" type="error"]We're doomed![/alert]``

Shortcut syntax: ``[alert="Shit happen" type="error"]We're doomed![/alert]``

Supported types:
- ``error``
- ``danger``
- ``warning``
- ``info``
- ``success``
- ``note``
- ``question``

N.B. Supported types can also be used as aliases.

Example: ``[error title="Shit happen"]We're doomed![/error]``

Default HTML templates require the ``panel`` and ``media object`` CSS components from the bootstrap web framework 
(version 3.x) and the latest version of the Font-Awesome web icons framework.

#### Code block

Tag name: ``code`` (alias: see below)

Supported attributes: ``language`` (alias: tag name), ``hl_lines``, ``linenostart``, ``filename``, ``src``, ``id``.

Syntax: ``[code language="python"]# Python code here[/code]``

Shortcut syntax: ``[code="python"]# Python code here[/code]``

Attributes usage (all optional):
- ``hl_lines``: Comma separated list of line numbers to be highlighted.
- ``linenostart``: First line number.
- ``filename``: Source file name.
- ``src``: Source file link URL.
- ``id``: enable HTML anchors on lines (format ``id-linenum`` and on the whole code block.

Shortcuts for commonly used programming languages:
- ``python``
- ``cpp``
- ``java``
- ``html``
- ``php``

Example: ``[python]# Python code here[/python]``

To add an horizontal scrollbar to all code blocks in HTML use :

```
.codetable {
    width:100%;
    height: auto;
    overflow: auto;
}
```

Default HTML templates require the ``panel`` CSS components from the bootstrap web framework 
(version 3.x) and the latest version of the Font-Awesome web icons framework.

**The [Pygments](http://pygments.org/) library MUST be installed.**

#### Definition list

Tags names: ``dl`` (list), ``dt`` (term), ``dd`` (definition)

Supported attribute: none.

Syntax: 
```
[dl]
[dt]Firefox[/dt]
[dd]Powerful web browser.[/dd]

[dt]Internet Explorer[/dt]
[dd]Relic of the past.[/dd]
[/dl]
```

N.B. A single term can have multiple definitions.

#### Electronic NOT notation (line above text)

Tag name: ``not``

Supported attribute: none.

Syntax: ``Pull the [not]RESET[/not] pin to low to reset.``

#### Figure

Tag name: ``figure`` (figure), ``figcaption`` (legend)

Supported attribute: ``id`` (alias: tag name) for ``figure``.

Syntax: ``[figure]Example figure[/figure]``
Syntax: ``[figure]Example figure[figcaption]With a legend[/figcaption][/figure]``

Syntax: ``[figure id="example-figure"]Example figure[/figure]``
Shortcut syntax: ``[figure="example-figure"]Example figure[/figure]``

#### Footnote

Tag name: ``footnote`` (alias: ``fn``), ``fnref`` (reference to a footnote)

Supported attribute: ``id`` (alias: tag name) for ``footnote``.

Syntax: ``This is a footnote[footnote id="first-footnote"]A this is the text of the footnote.[/footnote].``
Syntax: ``This is a reference to another footnote[fnref]first-footnote[/fnref].``

If the ID is not specified, an incremental counter (per document) is used.

#### Verbatim, aka "no parse"

Tag name: ``noparse`` (alias: ``nobbc``)

Supported attribute: none.

Syntax: ``[noparse]This will be displayed [b]as-is[/b] with tags.[/noparse]``

#### External link

Tag name: ``url`` (alias: ``link``)

Supported attribute: tag name.

N.B. Multi-format tag!

Syntax without text: ``See [url]http://github.com/TamiaLab[/url] for more information.``

Syntax with text: ``See [url=http://github.com/TamiaLab]the TamiaLab GitHub page[/url] for more information.``

#### Email link 

Tag name: ``email``

Supported attribute: tag name.

N.B. Multi-format tag!

Syntax without text: ``Contact [email]john.doe@example.com[/email] for more information.``

Syntax with text: ``See [email=john.doe@example.com]John Doe[/email] for more information.``

#### Anchor

Tag name: ``anchor``

Supported attribute: none.

Syntax: ``"I want to play a game."[anchor]cite-saw[/anchor]``

#### Internal link (go-to anchor)

Tag name: ``goto``

Supported attribute: ``id`` (alias: tag name).

Syntax: ``Like the [goto id="cite-saw"]famous sentence previously named[/goto].``

Shortcut syntax: ``Like the [goto="cite-saw"]famous sentence previously named[/goto].``

#### Generic list

Tag name: ``list``

Supported attribute: ``type`` (alias: tag name).

Supported types:
- ``1``: Numeric list
- ``a``: Lowercase list
- ``A``: Uppercase list
- ``I``: Roman uppercase list
- ``i``: Roman lowercase list

Fallback to an **unordered** list if ``type`` is not specified.

Syntax: 
```
[list type="1"]
[li]Red[/li]
[li]Green[/li]
[li]Blue[/li]
[li]Yellow[/li]
[/list]
```

#### Ordered list

Tag name: ``ol``

Supported attribute: ``type`` (alias: tag name).

Supported types:
- ``1``: Numeric list
- ``a``: Lowercase list
- ``A``: Uppercase list
- ``I``: Roman uppercase list
- ``i``: Roman lowercase list

Fallback to a **numeric** list if ``type`` is not specified.

Syntax: 
```
[ol type="1"]
[li]Red[/li]
[li]Green[/li]
[li]Blue[/li]
[li]Yellow[/li]
[/ol]
```

#### Unordered list

Tag name: ``ul``

Supported attribute: none. 

Syntax: 
```
[ul]
[li]Red[/li]
[li]Green[/li]
[li]Blue[/li]
[li]Yellow[/li]
[/ul]
```

#### List item

Tag name: ``li``

Supported attribute: none. 

Syntax: see examples above.

#### Image

Tag name: ``img``

Supported attribute: ``alt``, ``width`` (in pixels), ``height`` (in pixels).

N.B. All attributes are optional, but ``alt`` is strongly recommended.

Syntax: ``[img alt="Example image"]http://example.com/image.jpg[/img]``

#### Youtube video

Tag name: ``youtube``

Supported attribute: none.

Syntax: ``[youtube]https://www.youtube.com/watch?v=dQw4w9WgXcQ[/youtube]``

#### Quote

Tag name: ``quote`` (alias: ``blockquote``)

Supported attribute: ``author`` (alias: tag name), ``link``, ``date`` (unix timestamp).

N.B. All attributes are optional, but ``author`` is strongly recommended.

Syntax: ``[quote author="Skywodd"]I'm a penguin.[/quote]``

Shortcut syntax: ``[quote="Skywodd"]I'm a penguin.[/quote]``

#### Spoiler

Tag name: ``spoiler`` (alias: ``hide``)

Supported attribute: none.

Syntax: ``[spoiler]Harry Potter die at the end.[/spoiler]``

Example of Javascript (use Jquery) for the hide/show button :

```
$(".spoiler").each(function(index) {
	var t = $(this);
	t.hide();
	var l = $('<div><input type="button" value="Show spoiler"></div>');
	l.insertBefore($(this));
	l.click(function() {
		t.show();
		$(this).hide();
	});
});
```

#### Table

Tag name: ``table``, ``tr``, ``th``, ``td``

Supported attribute: ``colspan`` and ``rowspan`` for ``td`` and ``th``.

Syntax: 
```
[table]
[tr]
[th]Column 1[/th]
[th]Column 2[/th]
[th]Column 3[/th]
[/tr]
[tr]
[td]Cell 1-1[/td]
[td]Cell 1-2[/td]
[td]Cell 1-3[/td]
[/tr]
[tr]
[td]Cell 2-1[/td]
[td]Cell 2-2[/td]
[td]Cell 2-3[/td]
[/tr]
[/table]
```

N.B. Text version rendering not yet implemented.

#### Text alignement

Tag name: ``center``, ``left``, ``right``

Supported attribute: none.

Syntax: ``[center]Text centered[/center]``

Syntax: ``[left]Text left aligned[/left]``

Syntax: ``[right]Text right aligned[/right]``

#### Text colors

Tag name: ``color``

Supported attribute: tag name.

Currently support HEX color code and HTML color name as defined by [the W3C](https://www.w3.org/TR/CSS21/syndata.html#value-def-color).

Syntax: ``[color=#B8B8B8]Text in light gray.[/color]``

Shortcut syntax for common color : 
- ``black``
- ``blue``
- ``gray``
- ``green``
- ``orange``
- ``purple``
- ``red``
- ``white``
- ``yellow``

Example: ``[green]I love green.[/green]``

#### Text direction

Tag name: ``bdo``, ``ltr``, ``rtl``

Supported attribute: ``dir`` (alias: tag name) for ``bdo``.

Syntax: ``[bdo dir="ltr"]Left-to-right text[/bdo]``

Shortcut syntax: ``[bdo="ltr"]Left-to-right text[/bdo]``

Shortcut syntax for LTR: ``[ltr]Left-to-right text[/ltr]``

Shortcut syntax for RTL: ``[rtl]Right-to-left text[/rtl]``

#### Text formating

##### Bold

Tag name: ``b`` (aliases: ``bold``, ``strong``)

Supported attribute: none.

Syntax: ``[b]Bold text[/b]``

##### Italic

Tag name: ``i`` (aliases: ``italic``, ``em``)

Supported attribute: none.

Syntax: ``[i]Italic text[/i]``

##### Strike
 
Tag name: ``s`` (aliases: ``strike``, ``del``)

Supported attribute: none.

Syntax: ``[s]Strike text[/s]``

##### Underline
 
Tag name: ``u`` (aliases: ``underline``, ``ins``)

Supported attribute: none.

Syntax: ``[u]Underline text[/u]``

##### Subscript and superscript

Tag name: ``sub``, ``sup``

Supported attribute: none.

Syntax: ``[sub]Subscript text[/sub]``

Syntax: ``[sup]Superscript text[/sup]``

##### Monospace block
  
Tag name: ``pre``

Supported attribute: none.

Syntax: ``[pre]Monospaced text[/pre]``

##### Inline citation
  
Tag name: ``cite``

Supported attribute: none.

Syntax: ``The film [cite]Matrix[/cite] was really good.``

##### Inline code block

Tag name: ``icode``

Supported attribute: none.

Syntax: ``[icode]some_code[/icode]``

This tag, like the code blocks tag, is a "no parse" tag. Inner tags will **not** be processed, but displayed as-is instead.

##### Inline spoiler

Tag name: ``ispoiler``

Supported attribute: none.

Syntax: ``[ispoiler]I see you.[/ispoiler]``

Example of Javascript (use Jquery) for the hide/show button :

```
$(".ispoiler").each(function(index) {
	var t = $(this);
	t.hide();
	var l = $('<input type="button" value="Show spoiler">');
	l.insertBefore($(this));
	l.click(function() {
		t.show();
		$(this).hide();
	});
});
```

##### Keyboard shortcut

Tag name: ``kbd`` (alias: ``keyboard``)

Supported attribute: none.

Syntax: ``[kbd]CTRL + F[/kbd]``

##### Highlight 

Tag name: ``glow`` (aliases: ``mark``, ``highlight``)

Supported attribute: none.

Syntax: ``[mark]Keep this in mind.[/mark]``

##### Small text

Tag name: ``small``

Supported attribute: none.

Syntax: ``[small]* By accepting the ToS, you accept to give your soul to the devil for free.[/small]``

#### Text modifiers

Tag name: ``lowercase``, ``uppercase``, ``capitalize``

Supported attribute: none.

Syntax: ``[lowercase]Text will be lowercase.[/lowercase]``

Syntax: ``[uppercase]Text will be in UPPERCASE.[/uppercase]``

Syntax: ``[capitalize]Text will be capitalized.[/capitalize]``

#### Titles

Tag name: ``h1``, ``h2``, ``h3``, ``h4``, ``h5``, ``h6`` 

Supported attribute: ``id`` (alias: tag name, optional).

N.B. ``id`` can be used to attach a custom anchor ID to the title (permalink link).

Syntax: ``[h1]The first level title[/h1]``

Syntax: ``[h1 id="starwars_intro"]In a galaxy far far away ...[/h1]``

Shortcut syntax: ``[h1="starwars_intro"]In a galaxy far far away ...[/h1]``

#### TODO list

Tag name: ``todolist``, ``task``

Supported attribute: ``done`` for task (standalone attribute, no value required).

Syntax: 
```
[todolist]
[task done]Implement TODO list tag.[/task]
[task]Be rich.[/task]
[task]Be super rich.[/task]
[/todolist]
```

Tag name can also be used to mark the task as "done" : ``[task="done"]Implement TODO list tag.[/task]``

Example CSS for the TODO lists (require Font-Awesome):

```
.task_done {
    text-decoration: line-through;
    list-style-type: none;
}

.task_done p:before {
    font-family: FontAwesome;
    content:'\f046';
    display: inline-block;
    padding-right: 3px;
    vertical-align: middle;
}

.task_pending {
    list-style-type: none;
}

.task_pending p:before {
    font-family: FontAwesome;
    content:'\f096';
    display: inline-block;
    padding-right: 3px;
    vertical-align: middle;
}
```

#### Horizontal line

Tag name: ``hr``

Supported attribute: none.

Syntax: ``[hr]``

#### Line break

Tag name: ``br``

Supported attribute: none.

Syntax: ``First line.[br]Second line.``

#### "Cut Here" marker

Tag name: ``cuthere``

Supported attribute: none.

Generate a "Cut Here" marker as HTML comment for custom content preview processing.

Syntax: 
```
First paragraph, before the marker.

[cuthere]

Second paragraph, after the marker .
```

#### Nota Bene

Tag name: ``notabene`` (alias: ``nb``)

Supported attribute: ``important`` (alias: tag value).

Syntax: ``[notabene]Don't do this at home[/notabene]``

Syntax: ``[notabene important]Don't do this at home[/notabene]``

Syntax (using tag value): ``[notabene="important"]Don't do this at home[/notabene]``

#### Post scriptum

Tag name: ``postscriptum`` (alias: ``ps``)

Supported attribute: ``important`` (alias: tag value).

Syntax: ``[postscriptum]Don't do this at home[/postscriptum]``

Syntax: ``[postscriptum important]Don't do this at home[/postscriptum]``

Syntax (using tag value): ``[postscriptum="important"]Don't do this at home[/postscriptum]``
