<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US">
<head>
<link rel="icon" href="/cpython/static/hgicon.png" type="image/png" />
<meta name="robots" content="index, nofollow" />
<link rel="stylesheet" href="/cpython/static/style-paper.css" type="text/css" />
<script type="text/javascript" src="/cpython/static/mercurial.js"></script>

<link rel="stylesheet" href="/cpython/highlightcss" type="text/css" />
<title>cpython: 3b91d834160f Lib/HTMLParser.py</title>
</head>
<body>

<div class="container">
<div class="menu">
<div class="logo">
<a href="https://hg.python.org">
<img src="/cpython/static/hglogo.png" alt="back to hg.python.org repositories" /></a>
</div>
<ul>
<li><a href="/cpython/shortlog/3b91d834160f">log</a></li>
<li><a href="/cpython/graph/3b91d834160f">graph</a></li>
<li><a href="/cpython/tags">tags</a></li>
<li><a href="/cpython/branches">branches</a></li>
</ul>
<ul>
<li><a href="/cpython/rev/3b91d834160f">changeset</a></li>
<li><a href="/cpython/file/3b91d834160f/Lib/">browse</a></li>
</ul>
<ul>
<li class="active">file</li>
<li><a href="/cpython/file/tip/Lib/HTMLParser.py">latest</a></li>
<li><a href="/cpython/diff/3b91d834160f/Lib/HTMLParser.py">diff</a></li>
<li><a href="/cpython/comparison/3b91d834160f/Lib/HTMLParser.py">comparison</a></li>
<li><a href="/cpython/annotate/3b91d834160f/Lib/HTMLParser.py">annotate</a></li>
<li><a href="/cpython/log/3b91d834160f/Lib/HTMLParser.py">file log</a></li>
<li><a href="/cpython/raw-file/3b91d834160f/Lib/HTMLParser.py">raw</a></li>
</ul>
<ul>
<li><a href="/cpython/help">help</a></li>
</ul>
</div>

<div class="main">
<h2 class="breadcrumb"><a href="/">Mercurial</a> &gt; <a href="/cpython">cpython</a> </h2>
<h3>view Lib/HTMLParser.py @ 94984:3b91d834160f</h3>

<form class="search" action="/cpython/log">

<p><input name="rev" id="search1" type="text" size="30" /></p>
<div id="hint">Find changesets by keywords (author, files, the commit message), revision
number or hash, or <a href="/cpython/help/revsets">revset expression</a>.</div>
</form>

<div class="description">the default is sys.maxsize not sys.maxint (closes #23645)</a> [<a href="http://bugs.python.org/23645" class="issuelink">#23645</a>]</div>

<table id="changesetEntry">
<tr>
 <th class="author">author</th>
 <td class="author">&#66;&#101;&#110;&#106;&#97;&#109;&#105;&#110;&#32;&#80;&#101;&#116;&#101;&#114;&#115;&#111;&#110;&#32;&#60;&#98;&#101;&#110;&#106;&#97;&#109;&#105;&#110;&#64;&#112;&#121;&#116;&#104;&#111;&#110;&#46;&#111;&#114;&#103;&#62;</td>
</tr>
<tr>
 <th class="date">date</th>
 <td class="date age">Fri, 13 Mar 2015 14:32:31 -0500</td>
</tr>
<tr>
 <th class="author">parents</th>
 <td class="author"><a href="/cpython/file/695f988824bb/Lib/HTMLParser.py">695f988824bb</a> </td>
</tr>
<tr>
 <th class="author">children</th>
 <td class="author"></td>
</tr>
</table>

<div class="overflow">
<div class="sourcefirst linewraptoggle">line wrap: <a class="linewraplink" href="javascript:toggleLinewrap()">on</a></div>
<div class="sourcefirst"> line source</div>
<pre class="sourcelines stripes4 wrap">
<span id="l1"><span class="sd">&quot;&quot;&quot;A parser for HTML and XHTML.&quot;&quot;&quot;</span></span><a href="#l1"></a>
<span id="l2"></span><a href="#l2"></a>
<span id="l3"><span class="c"># This file is based on sgmllib.py, but the API is slightly different.</span></span><a href="#l3"></a>
<span id="l4"></span><a href="#l4"></a>
<span id="l5"><span class="c"># XXX There should be a way to distinguish between PCDATA (parsed</span></span><a href="#l5"></a>
<span id="l6"><span class="c"># character data -- the normal case), RCDATA (replaceable character</span></span><a href="#l6"></a>
<span id="l7"><span class="c"># data -- only char and entity references and end tags are special)</span></span><a href="#l7"></a>
<span id="l8"><span class="c"># and CDATA (character data -- only end tags are special).</span></span><a href="#l8"></a>
<span id="l9"></span><a href="#l9"></a>
<span id="l10"></span><a href="#l10"></a>
<span id="l11"><span class="kn">import</span> <span class="nn">markupbase</span></span><a href="#l11"></a>
<span id="l12"><span class="kn">import</span> <span class="nn">re</span></span><a href="#l12"></a>
<span id="l13"></span><a href="#l13"></a>
<span id="l14"><span class="c"># Regular expressions used for parsing</span></span><a href="#l14"></a>
<span id="l15"></span><a href="#l15"></a>
<span id="l16"><span class="n">interesting_normal</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s">&#39;[&amp;&lt;]&#39;</span><span class="p">)</span></span><a href="#l16"></a>
<span id="l17"><span class="n">incomplete</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s">&#39;&amp;[a-zA-Z#]&#39;</span><span class="p">)</span></span><a href="#l17"></a>
<span id="l18"></span><a href="#l18"></a>
<span id="l19"><span class="n">entityref</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s">&#39;&amp;([a-zA-Z][-.a-zA-Z0-9]*)[^a-zA-Z0-9]&#39;</span><span class="p">)</span></span><a href="#l19"></a>
<span id="l20"><span class="n">charref</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s">&#39;&amp;#(?:[0-9]+|[xX][0-9a-fA-F]+)[^0-9a-fA-F]&#39;</span><span class="p">)</span></span><a href="#l20"></a>
<span id="l21"></span><a href="#l21"></a>
<span id="l22"><span class="n">starttagopen</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s">&#39;&lt;[a-zA-Z]&#39;</span><span class="p">)</span></span><a href="#l22"></a>
<span id="l23"><span class="n">piclose</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s">&#39;&gt;&#39;</span><span class="p">)</span></span><a href="#l23"></a>
<span id="l24"><span class="n">commentclose</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s">r&#39;--\s*&gt;&#39;</span><span class="p">)</span></span><a href="#l24"></a>
<span id="l25"></span><a href="#l25"></a>
<span id="l26"><span class="c"># see http://www.w3.org/TR/html5/tokenization.html#tag-open-state</span></span><a href="#l26"></a>
<span id="l27"><span class="c"># and http://www.w3.org/TR/html5/tokenization.html#tag-name-state</span></span><a href="#l27"></a>
<span id="l28"><span class="c"># note: if you change tagfind/attrfind remember to update locatestarttagend too</span></span><a href="#l28"></a>
<span id="l29"><span class="n">tagfind</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s">&#39;([a-zA-Z][^</span><span class="se">\t\n\r\f</span><span class="s"> /&gt;</span><span class="se">\x00</span><span class="s">]*)(?:\s|/(?!&gt;))*&#39;</span><span class="p">)</span></span><a href="#l29"></a>
<span id="l30"><span class="c"># this regex is currently unused, but left for backward compatibility</span></span><a href="#l30"></a>
<span id="l31"><span class="n">tagfind_tolerant</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s">&#39;[a-zA-Z][^</span><span class="se">\t\n\r\f</span><span class="s"> /&gt;</span><span class="se">\x00</span><span class="s">]*&#39;</span><span class="p">)</span></span><a href="#l31"></a>
<span id="l32"></span><a href="#l32"></a>
<span id="l33"><span class="n">attrfind</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span></span><a href="#l33"></a>
<span id="l34">    <span class="s">r&#39;((?&lt;=[</span><span class="se">\&#39;</span><span class="s">&quot;\s/])[^\s/&gt;][^\s/=&gt;]*)(\s*=+\s*&#39;</span></span><a href="#l34"></a>
<span id="l35">    <span class="s">r&#39;(</span><span class="se">\&#39;</span><span class="s">[^</span><span class="se">\&#39;</span><span class="s">]*</span><span class="se">\&#39;</span><span class="s">|&quot;[^&quot;]*&quot;|(?![</span><span class="se">\&#39;</span><span class="s">&quot;])[^&gt;\s]*))?(?:\s|/(?!&gt;))*&#39;</span><span class="p">)</span></span><a href="#l35"></a>
<span id="l36"></span><a href="#l36"></a>
<span id="l37"><span class="n">locatestarttagend</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s">r&quot;&quot;&quot;</span></span><a href="#l37"></a>
<span id="l38"><span class="s">  &lt;[a-zA-Z][^\t\n\r\f /&gt;\x00]*       # tag name</span></span><a href="#l38"></a>
<span id="l39"><span class="s">  (?:[\s/]*                          # optional whitespace before attribute name</span></span><a href="#l39"></a>
<span id="l40"><span class="s">    (?:(?&lt;=[&#39;&quot;\s/])[^\s/&gt;][^\s/=&gt;]*  # attribute name</span></span><a href="#l40"></a>
<span id="l41"><span class="s">      (?:\s*=+\s*                    # value indicator</span></span><a href="#l41"></a>
<span id="l42"><span class="s">        (?:&#39;[^&#39;]*&#39;                   # LITA-enclosed value</span></span><a href="#l42"></a>
<span id="l43"><span class="s">          |&quot;[^&quot;]*&quot;                   # LIT-enclosed value</span></span><a href="#l43"></a>
<span id="l44"><span class="s">          |(?![&#39;&quot;])[^&gt;\s]*           # bare value</span></span><a href="#l44"></a>
<span id="l45"><span class="s">         )</span></span><a href="#l45"></a>
<span id="l46"><span class="s">       )?(?:\s|/(?!&gt;))*</span></span><a href="#l46"></a>
<span id="l47"><span class="s">     )*</span></span><a href="#l47"></a>
<span id="l48"><span class="s">   )?</span></span><a href="#l48"></a>
<span id="l49"><span class="s">  \s*                                # trailing whitespace</span></span><a href="#l49"></a>
<span id="l50"><span class="s">&quot;&quot;&quot;</span><span class="p">,</span> <span class="n">re</span><span class="o">.</span><span class="n">VERBOSE</span><span class="p">)</span></span><a href="#l50"></a>
<span id="l51"><span class="n">endendtag</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s">&#39;&gt;&#39;</span><span class="p">)</span></span><a href="#l51"></a>
<span id="l52"><span class="c"># the HTML 5 spec, section 8.1.2.2, doesn&#39;t allow spaces between</span></span><a href="#l52"></a>
<span id="l53"><span class="c"># &lt;/ and the tag name, so maybe this should be fixed</span></span><a href="#l53"></a>
<span id="l54"><span class="n">endtagfind</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s">&#39;&lt;/\s*([a-zA-Z][-.a-zA-Z0-9:_]*)\s*&gt;&#39;</span><span class="p">)</span></span><a href="#l54"></a>
<span id="l55"></span><a href="#l55"></a>
<span id="l56"></span><a href="#l56"></a>
<span id="l57"><span class="k">class</span> <span class="nc">HTMLParseError</span><span class="p">(</span><span class="ne">Exception</span><span class="p">):</span></span><a href="#l57"></a>
<span id="l58">    <span class="sd">&quot;&quot;&quot;Exception raised for all parse errors.&quot;&quot;&quot;</span></span><a href="#l58"></a>
<span id="l59"></span><a href="#l59"></a>
<span id="l60">    <span class="k">def</span> <span class="nf">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">msg</span><span class="p">,</span> <span class="n">position</span><span class="o">=</span><span class="p">(</span><span class="bp">None</span><span class="p">,</span> <span class="bp">None</span><span class="p">)):</span></span><a href="#l60"></a>
<span id="l61">        <span class="k">assert</span> <span class="n">msg</span></span><a href="#l61"></a>
<span id="l62">        <span class="bp">self</span><span class="o">.</span><span class="n">msg</span> <span class="o">=</span> <span class="n">msg</span></span><a href="#l62"></a>
<span id="l63">        <span class="bp">self</span><span class="o">.</span><span class="n">lineno</span> <span class="o">=</span> <span class="n">position</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span></span><a href="#l63"></a>
<span id="l64">        <span class="bp">self</span><span class="o">.</span><span class="n">offset</span> <span class="o">=</span> <span class="n">position</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span></span><a href="#l64"></a>
<span id="l65"></span><a href="#l65"></a>
<span id="l66">    <span class="k">def</span> <span class="nf">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></span><a href="#l66"></a>
<span id="l67">        <span class="n">result</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">msg</span></span><a href="#l67"></a>
<span id="l68">        <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">lineno</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l68"></a>
<span id="l69">            <span class="n">result</span> <span class="o">=</span> <span class="n">result</span> <span class="o">+</span> <span class="s">&quot;, at line </span><span class="si">%d</span><span class="s">&quot;</span> <span class="o">%</span> <span class="bp">self</span><span class="o">.</span><span class="n">lineno</span></span><a href="#l69"></a>
<span id="l70">        <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">offset</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l70"></a>
<span id="l71">            <span class="n">result</span> <span class="o">=</span> <span class="n">result</span> <span class="o">+</span> <span class="s">&quot;, column </span><span class="si">%d</span><span class="s">&quot;</span> <span class="o">%</span> <span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">offset</span> <span class="o">+</span> <span class="mi">1</span><span class="p">)</span></span><a href="#l71"></a>
<span id="l72">        <span class="k">return</span> <span class="n">result</span></span><a href="#l72"></a>
<span id="l73"></span><a href="#l73"></a>
<span id="l74"></span><a href="#l74"></a>
<span id="l75"><span class="k">class</span> <span class="nc">HTMLParser</span><span class="p">(</span><span class="n">markupbase</span><span class="o">.</span><span class="n">ParserBase</span><span class="p">):</span></span><a href="#l75"></a>
<span id="l76">    <span class="sd">&quot;&quot;&quot;Find tags and other markup and call handler functions.</span></span><a href="#l76"></a>
<span id="l77"></span><a href="#l77"></a>
<span id="l78"><span class="sd">    Usage:</span></span><a href="#l78"></a>
<span id="l79"><span class="sd">        p = HTMLParser()</span></span><a href="#l79"></a>
<span id="l80"><span class="sd">        p.feed(data)</span></span><a href="#l80"></a>
<span id="l81"><span class="sd">        ...</span></span><a href="#l81"></a>
<span id="l82"><span class="sd">        p.close()</span></span><a href="#l82"></a>
<span id="l83"></span><a href="#l83"></a>
<span id="l84"><span class="sd">    Start tags are handled by calling self.handle_starttag() or</span></span><a href="#l84"></a>
<span id="l85"><span class="sd">    self.handle_startendtag(); end tags by self.handle_endtag().  The</span></span><a href="#l85"></a>
<span id="l86"><span class="sd">    data between tags is passed from the parser to the derived class</span></span><a href="#l86"></a>
<span id="l87"><span class="sd">    by calling self.handle_data() with the data as argument (the data</span></span><a href="#l87"></a>
<span id="l88"><span class="sd">    may be split up in arbitrary chunks).  Entity references are</span></span><a href="#l88"></a>
<span id="l89"><span class="sd">    passed by calling self.handle_entityref() with the entity</span></span><a href="#l89"></a>
<span id="l90"><span class="sd">    reference as the argument.  Numeric character references are</span></span><a href="#l90"></a>
<span id="l91"><span class="sd">    passed to self.handle_charref() with the string containing the</span></span><a href="#l91"></a>
<span id="l92"><span class="sd">    reference as the argument.</span></span><a href="#l92"></a>
<span id="l93"><span class="sd">    &quot;&quot;&quot;</span></span><a href="#l93"></a>
<span id="l94"></span><a href="#l94"></a>
<span id="l95">    <span class="n">CDATA_CONTENT_ELEMENTS</span> <span class="o">=</span> <span class="p">(</span><span class="s">&quot;script&quot;</span><span class="p">,</span> <span class="s">&quot;style&quot;</span><span class="p">)</span></span><a href="#l95"></a>
<span id="l96"></span><a href="#l96"></a>
<span id="l97"></span><a href="#l97"></a>
<span id="l98">    <span class="k">def</span> <span class="nf">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></span><a href="#l98"></a>
<span id="l99">        <span class="sd">&quot;&quot;&quot;Initialize and reset this instance.&quot;&quot;&quot;</span></span><a href="#l99"></a>
<span id="l100">        <span class="bp">self</span><span class="o">.</span><span class="n">reset</span><span class="p">()</span></span><a href="#l100"></a>
<span id="l101"></span><a href="#l101"></a>
<span id="l102">    <span class="k">def</span> <span class="nf">reset</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></span><a href="#l102"></a>
<span id="l103">        <span class="sd">&quot;&quot;&quot;Reset this instance.  Loses all unprocessed data.&quot;&quot;&quot;</span></span><a href="#l103"></a>
<span id="l104">        <span class="bp">self</span><span class="o">.</span><span class="n">rawdata</span> <span class="o">=</span> <span class="s">&#39;&#39;</span></span><a href="#l104"></a>
<span id="l105">        <span class="bp">self</span><span class="o">.</span><span class="n">lasttag</span> <span class="o">=</span> <span class="s">&#39;???&#39;</span></span><a href="#l105"></a>
<span id="l106">        <span class="bp">self</span><span class="o">.</span><span class="n">interesting</span> <span class="o">=</span> <span class="n">interesting_normal</span></span><a href="#l106"></a>
<span id="l107">        <span class="bp">self</span><span class="o">.</span><span class="n">cdata_elem</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l107"></a>
<span id="l108">        <span class="n">markupbase</span><span class="o">.</span><span class="n">ParserBase</span><span class="o">.</span><span class="n">reset</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span></span><a href="#l108"></a>
<span id="l109"></span><a href="#l109"></a>
<span id="l110">    <span class="k">def</span> <span class="nf">feed</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">):</span></span><a href="#l110"></a>
<span id="l111">        <span class="sd">r&quot;&quot;&quot;Feed data to the parser.</span></span><a href="#l111"></a>
<span id="l112"></span><a href="#l112"></a>
<span id="l113"><span class="sd">        Call this as often as you want, with as little or as much text</span></span><a href="#l113"></a>
<span id="l114"><span class="sd">        as you want (may include &#39;\n&#39;).</span></span><a href="#l114"></a>
<span id="l115"><span class="sd">        &quot;&quot;&quot;</span></span><a href="#l115"></a>
<span id="l116">        <span class="bp">self</span><span class="o">.</span><span class="n">rawdata</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">rawdata</span> <span class="o">+</span> <span class="n">data</span></span><a href="#l116"></a>
<span id="l117">        <span class="bp">self</span><span class="o">.</span><span class="n">goahead</span><span class="p">(</span><span class="mi">0</span><span class="p">)</span></span><a href="#l117"></a>
<span id="l118"></span><a href="#l118"></a>
<span id="l119">    <span class="k">def</span> <span class="nf">close</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></span><a href="#l119"></a>
<span id="l120">        <span class="sd">&quot;&quot;&quot;Handle any buffered data.&quot;&quot;&quot;</span></span><a href="#l120"></a>
<span id="l121">        <span class="bp">self</span><span class="o">.</span><span class="n">goahead</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span></span><a href="#l121"></a>
<span id="l122"></span><a href="#l122"></a>
<span id="l123">    <span class="k">def</span> <span class="nf">error</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">message</span><span class="p">):</span></span><a href="#l123"></a>
<span id="l124">        <span class="k">raise</span> <span class="n">HTMLParseError</span><span class="p">(</span><span class="n">message</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">getpos</span><span class="p">())</span></span><a href="#l124"></a>
<span id="l125"></span><a href="#l125"></a>
<span id="l126">    <span class="n">__starttag_text</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l126"></a>
<span id="l127"></span><a href="#l127"></a>
<span id="l128">    <span class="k">def</span> <span class="nf">get_starttag_text</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></span><a href="#l128"></a>
<span id="l129">        <span class="sd">&quot;&quot;&quot;Return full source of start tag: &#39;&lt;...&gt;&#39;.&quot;&quot;&quot;</span></span><a href="#l129"></a>
<span id="l130">        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">__starttag_text</span></span><a href="#l130"></a>
<span id="l131"></span><a href="#l131"></a>
<span id="l132">    <span class="k">def</span> <span class="nf">set_cdata_mode</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">elem</span><span class="p">):</span></span><a href="#l132"></a>
<span id="l133">        <span class="bp">self</span><span class="o">.</span><span class="n">cdata_elem</span> <span class="o">=</span> <span class="n">elem</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span></span><a href="#l133"></a>
<span id="l134">        <span class="bp">self</span><span class="o">.</span><span class="n">interesting</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s">r&#39;&lt;/\s*</span><span class="si">%s</span><span class="s">\s*&gt;&#39;</span> <span class="o">%</span> <span class="bp">self</span><span class="o">.</span><span class="n">cdata_elem</span><span class="p">,</span> <span class="n">re</span><span class="o">.</span><span class="n">I</span><span class="p">)</span></span><a href="#l134"></a>
<span id="l135"></span><a href="#l135"></a>
<span id="l136">    <span class="k">def</span> <span class="nf">clear_cdata_mode</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span></span><a href="#l136"></a>
<span id="l137">        <span class="bp">self</span><span class="o">.</span><span class="n">interesting</span> <span class="o">=</span> <span class="n">interesting_normal</span></span><a href="#l137"></a>
<span id="l138">        <span class="bp">self</span><span class="o">.</span><span class="n">cdata_elem</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l138"></a>
<span id="l139"></span><a href="#l139"></a>
<span id="l140">    <span class="c"># Internal -- handle data as far as reasonable.  May leave state</span></span><a href="#l140"></a>
<span id="l141">    <span class="c"># and data to be processed by a subsequent call.  If &#39;end&#39; is</span></span><a href="#l141"></a>
<span id="l142">    <span class="c"># true, force handling all data as if followed by EOF marker.</span></span><a href="#l142"></a>
<span id="l143">    <span class="k">def</span> <span class="nf">goahead</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">end</span><span class="p">):</span></span><a href="#l143"></a>
<span id="l144">        <span class="n">rawdata</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">rawdata</span></span><a href="#l144"></a>
<span id="l145">        <span class="n">i</span> <span class="o">=</span> <span class="mi">0</span></span><a href="#l145"></a>
<span id="l146">        <span class="n">n</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">rawdata</span><span class="p">)</span></span><a href="#l146"></a>
<span id="l147">        <span class="k">while</span> <span class="n">i</span> <span class="o">&lt;</span> <span class="n">n</span><span class="p">:</span></span><a href="#l147"></a>
<span id="l148">            <span class="n">match</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">interesting</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">rawdata</span><span class="p">,</span> <span class="n">i</span><span class="p">)</span> <span class="c"># &lt; or &amp;</span></span><a href="#l148"></a>
<span id="l149">            <span class="k">if</span> <span class="n">match</span><span class="p">:</span></span><a href="#l149"></a>
<span id="l150">                <span class="n">j</span> <span class="o">=</span> <span class="n">match</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></span><a href="#l150"></a>
<span id="l151">            <span class="k">else</span><span class="p">:</span></span><a href="#l151"></a>
<span id="l152">                <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">cdata_elem</span><span class="p">:</span></span><a href="#l152"></a>
<span id="l153">                    <span class="k">break</span></span><a href="#l153"></a>
<span id="l154">                <span class="n">j</span> <span class="o">=</span> <span class="n">n</span></span><a href="#l154"></a>
<span id="l155">            <span class="k">if</span> <span class="n">i</span> <span class="o">&lt;</span> <span class="n">j</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">handle_data</span><span class="p">(</span><span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">j</span><span class="p">])</span></span><a href="#l155"></a>
<span id="l156">            <span class="n">i</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">updatepos</span><span class="p">(</span><span class="n">i</span><span class="p">,</span> <span class="n">j</span><span class="p">)</span></span><a href="#l156"></a>
<span id="l157">            <span class="k">if</span> <span class="n">i</span> <span class="o">==</span> <span class="n">n</span><span class="p">:</span> <span class="k">break</span></span><a href="#l157"></a>
<span id="l158">            <span class="n">startswith</span> <span class="o">=</span> <span class="n">rawdata</span><span class="o">.</span><span class="n">startswith</span></span><a href="#l158"></a>
<span id="l159">            <span class="k">if</span> <span class="n">startswith</span><span class="p">(</span><span class="s">&#39;&lt;&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span></span><a href="#l159"></a>
<span id="l160">                <span class="k">if</span> <span class="n">starttagopen</span><span class="o">.</span><span class="n">match</span><span class="p">(</span><span class="n">rawdata</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span> <span class="c"># &lt; + letter</span></span><a href="#l160"></a>
<span id="l161">                    <span class="n">k</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">parse_starttag</span><span class="p">(</span><span class="n">i</span><span class="p">)</span></span><a href="#l161"></a>
<span id="l162">                <span class="k">elif</span> <span class="n">startswith</span><span class="p">(</span><span class="s">&quot;&lt;/&quot;</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span></span><a href="#l162"></a>
<span id="l163">                    <span class="n">k</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">parse_endtag</span><span class="p">(</span><span class="n">i</span><span class="p">)</span></span><a href="#l163"></a>
<span id="l164">                <span class="k">elif</span> <span class="n">startswith</span><span class="p">(</span><span class="s">&quot;&lt;!--&quot;</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span></span><a href="#l164"></a>
<span id="l165">                    <span class="n">k</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">parse_comment</span><span class="p">(</span><span class="n">i</span><span class="p">)</span></span><a href="#l165"></a>
<span id="l166">                <span class="k">elif</span> <span class="n">startswith</span><span class="p">(</span><span class="s">&quot;&lt;?&quot;</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span></span><a href="#l166"></a>
<span id="l167">                    <span class="n">k</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">parse_pi</span><span class="p">(</span><span class="n">i</span><span class="p">)</span></span><a href="#l167"></a>
<span id="l168">                <span class="k">elif</span> <span class="n">startswith</span><span class="p">(</span><span class="s">&quot;&lt;!&quot;</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span></span><a href="#l168"></a>
<span id="l169">                    <span class="n">k</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">parse_html_declaration</span><span class="p">(</span><span class="n">i</span><span class="p">)</span></span><a href="#l169"></a>
<span id="l170">                <span class="k">elif</span> <span class="p">(</span><span class="n">i</span> <span class="o">+</span> <span class="mi">1</span><span class="p">)</span> <span class="o">&lt;</span> <span class="n">n</span><span class="p">:</span></span><a href="#l170"></a>
<span id="l171">                    <span class="bp">self</span><span class="o">.</span><span class="n">handle_data</span><span class="p">(</span><span class="s">&quot;&lt;&quot;</span><span class="p">)</span></span><a href="#l171"></a>
<span id="l172">                    <span class="n">k</span> <span class="o">=</span> <span class="n">i</span> <span class="o">+</span> <span class="mi">1</span></span><a href="#l172"></a>
<span id="l173">                <span class="k">else</span><span class="p">:</span></span><a href="#l173"></a>
<span id="l174">                    <span class="k">break</span></span><a href="#l174"></a>
<span id="l175">                <span class="k">if</span> <span class="n">k</span> <span class="o">&lt;</span> <span class="mi">0</span><span class="p">:</span></span><a href="#l175"></a>
<span id="l176">                    <span class="k">if</span> <span class="ow">not</span> <span class="n">end</span><span class="p">:</span></span><a href="#l176"></a>
<span id="l177">                        <span class="k">break</span></span><a href="#l177"></a>
<span id="l178">                    <span class="n">k</span> <span class="o">=</span> <span class="n">rawdata</span><span class="o">.</span><span class="n">find</span><span class="p">(</span><span class="s">&#39;&gt;&#39;</span><span class="p">,</span> <span class="n">i</span> <span class="o">+</span> <span class="mi">1</span><span class="p">)</span></span><a href="#l178"></a>
<span id="l179">                    <span class="k">if</span> <span class="n">k</span> <span class="o">&lt;</span> <span class="mi">0</span><span class="p">:</span></span><a href="#l179"></a>
<span id="l180">                        <span class="n">k</span> <span class="o">=</span> <span class="n">rawdata</span><span class="o">.</span><span class="n">find</span><span class="p">(</span><span class="s">&#39;&lt;&#39;</span><span class="p">,</span> <span class="n">i</span> <span class="o">+</span> <span class="mi">1</span><span class="p">)</span></span><a href="#l180"></a>
<span id="l181">                        <span class="k">if</span> <span class="n">k</span> <span class="o">&lt;</span> <span class="mi">0</span><span class="p">:</span></span><a href="#l181"></a>
<span id="l182">                            <span class="n">k</span> <span class="o">=</span> <span class="n">i</span> <span class="o">+</span> <span class="mi">1</span></span><a href="#l182"></a>
<span id="l183">                    <span class="k">else</span><span class="p">:</span></span><a href="#l183"></a>
<span id="l184">                        <span class="n">k</span> <span class="o">+=</span> <span class="mi">1</span></span><a href="#l184"></a>
<span id="l185">                    <span class="bp">self</span><span class="o">.</span><span class="n">handle_data</span><span class="p">(</span><span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">k</span><span class="p">])</span></span><a href="#l185"></a>
<span id="l186">                <span class="n">i</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">updatepos</span><span class="p">(</span><span class="n">i</span><span class="p">,</span> <span class="n">k</span><span class="p">)</span></span><a href="#l186"></a>
<span id="l187">            <span class="k">elif</span> <span class="n">startswith</span><span class="p">(</span><span class="s">&quot;&amp;#&quot;</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span></span><a href="#l187"></a>
<span id="l188">                <span class="n">match</span> <span class="o">=</span> <span class="n">charref</span><span class="o">.</span><span class="n">match</span><span class="p">(</span><span class="n">rawdata</span><span class="p">,</span> <span class="n">i</span><span class="p">)</span></span><a href="#l188"></a>
<span id="l189">                <span class="k">if</span> <span class="n">match</span><span class="p">:</span></span><a href="#l189"></a>
<span id="l190">                    <span class="n">name</span> <span class="o">=</span> <span class="n">match</span><span class="o">.</span><span class="n">group</span><span class="p">()[</span><span class="mi">2</span><span class="p">:</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span></span><a href="#l190"></a>
<span id="l191">                    <span class="bp">self</span><span class="o">.</span><span class="n">handle_charref</span><span class="p">(</span><span class="n">name</span><span class="p">)</span></span><a href="#l191"></a>
<span id="l192">                    <span class="n">k</span> <span class="o">=</span> <span class="n">match</span><span class="o">.</span><span class="n">end</span><span class="p">()</span></span><a href="#l192"></a>
<span id="l193">                    <span class="k">if</span> <span class="ow">not</span> <span class="n">startswith</span><span class="p">(</span><span class="s">&#39;;&#39;</span><span class="p">,</span> <span class="n">k</span><span class="o">-</span><span class="mi">1</span><span class="p">):</span></span><a href="#l193"></a>
<span id="l194">                        <span class="n">k</span> <span class="o">=</span> <span class="n">k</span> <span class="o">-</span> <span class="mi">1</span></span><a href="#l194"></a>
<span id="l195">                    <span class="n">i</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">updatepos</span><span class="p">(</span><span class="n">i</span><span class="p">,</span> <span class="n">k</span><span class="p">)</span></span><a href="#l195"></a>
<span id="l196">                    <span class="k">continue</span></span><a href="#l196"></a>
<span id="l197">                <span class="k">else</span><span class="p">:</span></span><a href="#l197"></a>
<span id="l198">                    <span class="k">if</span> <span class="s">&quot;;&quot;</span> <span class="ow">in</span> <span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:]:</span>  <span class="c"># bail by consuming &#39;&amp;#&#39;</span></span><a href="#l198"></a>
<span id="l199">                        <span class="bp">self</span><span class="o">.</span><span class="n">handle_data</span><span class="p">(</span><span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">i</span><span class="o">+</span><span class="mi">2</span><span class="p">])</span></span><a href="#l199"></a>
<span id="l200">                        <span class="n">i</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">updatepos</span><span class="p">(</span><span class="n">i</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">2</span><span class="p">)</span></span><a href="#l200"></a>
<span id="l201">                    <span class="k">break</span></span><a href="#l201"></a>
<span id="l202">            <span class="k">elif</span> <span class="n">startswith</span><span class="p">(</span><span class="s">&#39;&amp;&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span></span><a href="#l202"></a>
<span id="l203">                <span class="n">match</span> <span class="o">=</span> <span class="n">entityref</span><span class="o">.</span><span class="n">match</span><span class="p">(</span><span class="n">rawdata</span><span class="p">,</span> <span class="n">i</span><span class="p">)</span></span><a href="#l203"></a>
<span id="l204">                <span class="k">if</span> <span class="n">match</span><span class="p">:</span></span><a href="#l204"></a>
<span id="l205">                    <span class="n">name</span> <span class="o">=</span> <span class="n">match</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span></span><a href="#l205"></a>
<span id="l206">                    <span class="bp">self</span><span class="o">.</span><span class="n">handle_entityref</span><span class="p">(</span><span class="n">name</span><span class="p">)</span></span><a href="#l206"></a>
<span id="l207">                    <span class="n">k</span> <span class="o">=</span> <span class="n">match</span><span class="o">.</span><span class="n">end</span><span class="p">()</span></span><a href="#l207"></a>
<span id="l208">                    <span class="k">if</span> <span class="ow">not</span> <span class="n">startswith</span><span class="p">(</span><span class="s">&#39;;&#39;</span><span class="p">,</span> <span class="n">k</span><span class="o">-</span><span class="mi">1</span><span class="p">):</span></span><a href="#l208"></a>
<span id="l209">                        <span class="n">k</span> <span class="o">=</span> <span class="n">k</span> <span class="o">-</span> <span class="mi">1</span></span><a href="#l209"></a>
<span id="l210">                    <span class="n">i</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">updatepos</span><span class="p">(</span><span class="n">i</span><span class="p">,</span> <span class="n">k</span><span class="p">)</span></span><a href="#l210"></a>
<span id="l211">                    <span class="k">continue</span></span><a href="#l211"></a>
<span id="l212">                <span class="n">match</span> <span class="o">=</span> <span class="n">incomplete</span><span class="o">.</span><span class="n">match</span><span class="p">(</span><span class="n">rawdata</span><span class="p">,</span> <span class="n">i</span><span class="p">)</span></span><a href="#l212"></a>
<span id="l213">                <span class="k">if</span> <span class="n">match</span><span class="p">:</span></span><a href="#l213"></a>
<span id="l214">                    <span class="c"># match.group() will contain at least 2 chars</span></span><a href="#l214"></a>
<span id="l215">                    <span class="k">if</span> <span class="n">end</span> <span class="ow">and</span> <span class="n">match</span><span class="o">.</span><span class="n">group</span><span class="p">()</span> <span class="o">==</span> <span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:]:</span></span><a href="#l215"></a>
<span id="l216">                        <span class="bp">self</span><span class="o">.</span><span class="n">error</span><span class="p">(</span><span class="s">&quot;EOF in middle of entity or char ref&quot;</span><span class="p">)</span></span><a href="#l216"></a>
<span id="l217">                    <span class="c"># incomplete</span></span><a href="#l217"></a>
<span id="l218">                    <span class="k">break</span></span><a href="#l218"></a>
<span id="l219">                <span class="k">elif</span> <span class="p">(</span><span class="n">i</span> <span class="o">+</span> <span class="mi">1</span><span class="p">)</span> <span class="o">&lt;</span> <span class="n">n</span><span class="p">:</span></span><a href="#l219"></a>
<span id="l220">                    <span class="c"># not the end of the buffer, and can&#39;t be confused</span></span><a href="#l220"></a>
<span id="l221">                    <span class="c"># with some other construct</span></span><a href="#l221"></a>
<span id="l222">                    <span class="bp">self</span><span class="o">.</span><span class="n">handle_data</span><span class="p">(</span><span class="s">&quot;&amp;&quot;</span><span class="p">)</span></span><a href="#l222"></a>
<span id="l223">                    <span class="n">i</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">updatepos</span><span class="p">(</span><span class="n">i</span><span class="p">,</span> <span class="n">i</span> <span class="o">+</span> <span class="mi">1</span><span class="p">)</span></span><a href="#l223"></a>
<span id="l224">                <span class="k">else</span><span class="p">:</span></span><a href="#l224"></a>
<span id="l225">                    <span class="k">break</span></span><a href="#l225"></a>
<span id="l226">            <span class="k">else</span><span class="p">:</span></span><a href="#l226"></a>
<span id="l227">                <span class="k">assert</span> <span class="mi">0</span><span class="p">,</span> <span class="s">&quot;interesting.search() lied&quot;</span></span><a href="#l227"></a>
<span id="l228">        <span class="c"># end while</span></span><a href="#l228"></a>
<span id="l229">        <span class="k">if</span> <span class="n">end</span> <span class="ow">and</span> <span class="n">i</span> <span class="o">&lt;</span> <span class="n">n</span> <span class="ow">and</span> <span class="ow">not</span> <span class="bp">self</span><span class="o">.</span><span class="n">cdata_elem</span><span class="p">:</span></span><a href="#l229"></a>
<span id="l230">            <span class="bp">self</span><span class="o">.</span><span class="n">handle_data</span><span class="p">(</span><span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">n</span><span class="p">])</span></span><a href="#l230"></a>
<span id="l231">            <span class="n">i</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">updatepos</span><span class="p">(</span><span class="n">i</span><span class="p">,</span> <span class="n">n</span><span class="p">)</span></span><a href="#l231"></a>
<span id="l232">        <span class="bp">self</span><span class="o">.</span><span class="n">rawdata</span> <span class="o">=</span> <span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:]</span></span><a href="#l232"></a>
<span id="l233"></span><a href="#l233"></a>
<span id="l234">    <span class="c"># Internal -- parse html declarations, return length or -1 if not terminated</span></span><a href="#l234"></a>
<span id="l235">    <span class="c"># See w3.org/TR/html5/tokenization.html#markup-declaration-open-state</span></span><a href="#l235"></a>
<span id="l236">    <span class="c"># See also parse_declaration in _markupbase</span></span><a href="#l236"></a>
<span id="l237">    <span class="k">def</span> <span class="nf">parse_html_declaration</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span></span><a href="#l237"></a>
<span id="l238">        <span class="n">rawdata</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">rawdata</span></span><a href="#l238"></a>
<span id="l239">        <span class="k">if</span> <span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">i</span><span class="o">+</span><span class="mi">2</span><span class="p">]</span> <span class="o">!=</span> <span class="s">&#39;&lt;!&#39;</span><span class="p">:</span></span><a href="#l239"></a>
<span id="l240">            <span class="bp">self</span><span class="o">.</span><span class="n">error</span><span class="p">(</span><span class="s">&#39;unexpected call to parse_html_declaration()&#39;</span><span class="p">)</span></span><a href="#l240"></a>
<span id="l241">        <span class="k">if</span> <span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">i</span><span class="o">+</span><span class="mi">4</span><span class="p">]</span> <span class="o">==</span> <span class="s">&#39;&lt;!--&#39;</span><span class="p">:</span></span><a href="#l241"></a>
<span id="l242">            <span class="c"># this case is actually already handled in goahead()</span></span><a href="#l242"></a>
<span id="l243">            <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">parse_comment</span><span class="p">(</span><span class="n">i</span><span class="p">)</span></span><a href="#l243"></a>
<span id="l244">        <span class="k">elif</span> <span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">i</span><span class="o">+</span><span class="mi">3</span><span class="p">]</span> <span class="o">==</span> <span class="s">&#39;&lt;![&#39;</span><span class="p">:</span></span><a href="#l244"></a>
<span id="l245">            <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">parse_marked_section</span><span class="p">(</span><span class="n">i</span><span class="p">)</span></span><a href="#l245"></a>
<span id="l246">        <span class="k">elif</span> <span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">i</span><span class="o">+</span><span class="mi">9</span><span class="p">]</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span> <span class="o">==</span> <span class="s">&#39;&lt;!doctype&#39;</span><span class="p">:</span></span><a href="#l246"></a>
<span id="l247">            <span class="c"># find the closing &gt;</span></span><a href="#l247"></a>
<span id="l248">            <span class="n">gtpos</span> <span class="o">=</span> <span class="n">rawdata</span><span class="o">.</span><span class="n">find</span><span class="p">(</span><span class="s">&#39;&gt;&#39;</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">9</span><span class="p">)</span></span><a href="#l248"></a>
<span id="l249">            <span class="k">if</span> <span class="n">gtpos</span> <span class="o">==</span> <span class="o">-</span><span class="mi">1</span><span class="p">:</span></span><a href="#l249"></a>
<span id="l250">                <span class="k">return</span> <span class="o">-</span><span class="mi">1</span></span><a href="#l250"></a>
<span id="l251">            <span class="bp">self</span><span class="o">.</span><span class="n">handle_decl</span><span class="p">(</span><span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="o">+</span><span class="mi">2</span><span class="p">:</span><span class="n">gtpos</span><span class="p">])</span></span><a href="#l251"></a>
<span id="l252">            <span class="k">return</span> <span class="n">gtpos</span><span class="o">+</span><span class="mi">1</span></span><a href="#l252"></a>
<span id="l253">        <span class="k">else</span><span class="p">:</span></span><a href="#l253"></a>
<span id="l254">            <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">parse_bogus_comment</span><span class="p">(</span><span class="n">i</span><span class="p">)</span></span><a href="#l254"></a>
<span id="l255"></span><a href="#l255"></a>
<span id="l256">    <span class="c"># Internal -- parse bogus comment, return length or -1 if not terminated</span></span><a href="#l256"></a>
<span id="l257">    <span class="c"># see http://www.w3.org/TR/html5/tokenization.html#bogus-comment-state</span></span><a href="#l257"></a>
<span id="l258">    <span class="k">def</span> <span class="nf">parse_bogus_comment</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="n">report</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span></span><a href="#l258"></a>
<span id="l259">        <span class="n">rawdata</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">rawdata</span></span><a href="#l259"></a>
<span id="l260">        <span class="k">if</span> <span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">i</span><span class="o">+</span><span class="mi">2</span><span class="p">]</span> <span class="ow">not</span> <span class="ow">in</span> <span class="p">(</span><span class="s">&#39;&lt;!&#39;</span><span class="p">,</span> <span class="s">&#39;&lt;/&#39;</span><span class="p">):</span></span><a href="#l260"></a>
<span id="l261">            <span class="bp">self</span><span class="o">.</span><span class="n">error</span><span class="p">(</span><span class="s">&#39;unexpected call to parse_comment()&#39;</span><span class="p">)</span></span><a href="#l261"></a>
<span id="l262">        <span class="n">pos</span> <span class="o">=</span> <span class="n">rawdata</span><span class="o">.</span><span class="n">find</span><span class="p">(</span><span class="s">&#39;&gt;&#39;</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">2</span><span class="p">)</span></span><a href="#l262"></a>
<span id="l263">        <span class="k">if</span> <span class="n">pos</span> <span class="o">==</span> <span class="o">-</span><span class="mi">1</span><span class="p">:</span></span><a href="#l263"></a>
<span id="l264">            <span class="k">return</span> <span class="o">-</span><span class="mi">1</span></span><a href="#l264"></a>
<span id="l265">        <span class="k">if</span> <span class="n">report</span><span class="p">:</span></span><a href="#l265"></a>
<span id="l266">            <span class="bp">self</span><span class="o">.</span><span class="n">handle_comment</span><span class="p">(</span><span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="o">+</span><span class="mi">2</span><span class="p">:</span><span class="n">pos</span><span class="p">])</span></span><a href="#l266"></a>
<span id="l267">        <span class="k">return</span> <span class="n">pos</span> <span class="o">+</span> <span class="mi">1</span></span><a href="#l267"></a>
<span id="l268"></span><a href="#l268"></a>
<span id="l269">    <span class="c"># Internal -- parse processing instr, return end or -1 if not terminated</span></span><a href="#l269"></a>
<span id="l270">    <span class="k">def</span> <span class="nf">parse_pi</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span></span><a href="#l270"></a>
<span id="l271">        <span class="n">rawdata</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">rawdata</span></span><a href="#l271"></a>
<span id="l272">        <span class="k">assert</span> <span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">i</span><span class="o">+</span><span class="mi">2</span><span class="p">]</span> <span class="o">==</span> <span class="s">&#39;&lt;?&#39;</span><span class="p">,</span> <span class="s">&#39;unexpected call to parse_pi()&#39;</span></span><a href="#l272"></a>
<span id="l273">        <span class="n">match</span> <span class="o">=</span> <span class="n">piclose</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">rawdata</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">2</span><span class="p">)</span> <span class="c"># &gt;</span></span><a href="#l273"></a>
<span id="l274">        <span class="k">if</span> <span class="ow">not</span> <span class="n">match</span><span class="p">:</span></span><a href="#l274"></a>
<span id="l275">            <span class="k">return</span> <span class="o">-</span><span class="mi">1</span></span><a href="#l275"></a>
<span id="l276">        <span class="n">j</span> <span class="o">=</span> <span class="n">match</span><span class="o">.</span><span class="n">start</span><span class="p">()</span></span><a href="#l276"></a>
<span id="l277">        <span class="bp">self</span><span class="o">.</span><span class="n">handle_pi</span><span class="p">(</span><span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="o">+</span><span class="mi">2</span><span class="p">:</span> <span class="n">j</span><span class="p">])</span></span><a href="#l277"></a>
<span id="l278">        <span class="n">j</span> <span class="o">=</span> <span class="n">match</span><span class="o">.</span><span class="n">end</span><span class="p">()</span></span><a href="#l278"></a>
<span id="l279">        <span class="k">return</span> <span class="n">j</span></span><a href="#l279"></a>
<span id="l280"></span><a href="#l280"></a>
<span id="l281">    <span class="c"># Internal -- handle starttag, return end or -1 if not terminated</span></span><a href="#l281"></a>
<span id="l282">    <span class="k">def</span> <span class="nf">parse_starttag</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span></span><a href="#l282"></a>
<span id="l283">        <span class="bp">self</span><span class="o">.</span><span class="n">__starttag_text</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l283"></a>
<span id="l284">        <span class="n">endpos</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">check_for_whole_start_tag</span><span class="p">(</span><span class="n">i</span><span class="p">)</span></span><a href="#l284"></a>
<span id="l285">        <span class="k">if</span> <span class="n">endpos</span> <span class="o">&lt;</span> <span class="mi">0</span><span class="p">:</span></span><a href="#l285"></a>
<span id="l286">            <span class="k">return</span> <span class="n">endpos</span></span><a href="#l286"></a>
<span id="l287">        <span class="n">rawdata</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">rawdata</span></span><a href="#l287"></a>
<span id="l288">        <span class="bp">self</span><span class="o">.</span><span class="n">__starttag_text</span> <span class="o">=</span> <span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">endpos</span><span class="p">]</span></span><a href="#l288"></a>
<span id="l289"></span><a href="#l289"></a>
<span id="l290">        <span class="c"># Now parse the data between i+1 and j into a tag and attrs</span></span><a href="#l290"></a>
<span id="l291">        <span class="n">attrs</span> <span class="o">=</span> <span class="p">[]</span></span><a href="#l291"></a>
<span id="l292">        <span class="n">match</span> <span class="o">=</span> <span class="n">tagfind</span><span class="o">.</span><span class="n">match</span><span class="p">(</span><span class="n">rawdata</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">)</span></span><a href="#l292"></a>
<span id="l293">        <span class="k">assert</span> <span class="n">match</span><span class="p">,</span> <span class="s">&#39;unexpected call to parse_starttag()&#39;</span></span><a href="#l293"></a>
<span id="l294">        <span class="n">k</span> <span class="o">=</span> <span class="n">match</span><span class="o">.</span><span class="n">end</span><span class="p">()</span></span><a href="#l294"></a>
<span id="l295">        <span class="bp">self</span><span class="o">.</span><span class="n">lasttag</span> <span class="o">=</span> <span class="n">tag</span> <span class="o">=</span> <span class="n">match</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span></span><a href="#l295"></a>
<span id="l296"></span><a href="#l296"></a>
<span id="l297">        <span class="k">while</span> <span class="n">k</span> <span class="o">&lt;</span> <span class="n">endpos</span><span class="p">:</span></span><a href="#l297"></a>
<span id="l298">            <span class="n">m</span> <span class="o">=</span> <span class="n">attrfind</span><span class="o">.</span><span class="n">match</span><span class="p">(</span><span class="n">rawdata</span><span class="p">,</span> <span class="n">k</span><span class="p">)</span></span><a href="#l298"></a>
<span id="l299">            <span class="k">if</span> <span class="ow">not</span> <span class="n">m</span><span class="p">:</span></span><a href="#l299"></a>
<span id="l300">                <span class="k">break</span></span><a href="#l300"></a>
<span id="l301">            <span class="n">attrname</span><span class="p">,</span> <span class="n">rest</span><span class="p">,</span> <span class="n">attrvalue</span> <span class="o">=</span> <span class="n">m</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">)</span></span><a href="#l301"></a>
<span id="l302">            <span class="k">if</span> <span class="ow">not</span> <span class="n">rest</span><span class="p">:</span></span><a href="#l302"></a>
<span id="l303">                <span class="n">attrvalue</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l303"></a>
<span id="l304">            <span class="k">elif</span> <span class="n">attrvalue</span><span class="p">[:</span><span class="mi">1</span><span class="p">]</span> <span class="o">==</span> <span class="s">&#39;</span><span class="se">\&#39;</span><span class="s">&#39;</span> <span class="o">==</span> <span class="n">attrvalue</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">:]</span> <span class="ow">or</span> \</span><a href="#l304"></a>
<span id="l305">                 <span class="n">attrvalue</span><span class="p">[:</span><span class="mi">1</span><span class="p">]</span> <span class="o">==</span> <span class="s">&#39;&quot;&#39;</span> <span class="o">==</span> <span class="n">attrvalue</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">:]:</span></span><a href="#l305"></a>
<span id="l306">                <span class="n">attrvalue</span> <span class="o">=</span> <span class="n">attrvalue</span><span class="p">[</span><span class="mi">1</span><span class="p">:</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span></span><a href="#l306"></a>
<span id="l307">            <span class="k">if</span> <span class="n">attrvalue</span><span class="p">:</span></span><a href="#l307"></a>
<span id="l308">                <span class="n">attrvalue</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">unescape</span><span class="p">(</span><span class="n">attrvalue</span><span class="p">)</span></span><a href="#l308"></a>
<span id="l309">            <span class="n">attrs</span><span class="o">.</span><span class="n">append</span><span class="p">((</span><span class="n">attrname</span><span class="o">.</span><span class="n">lower</span><span class="p">(),</span> <span class="n">attrvalue</span><span class="p">))</span></span><a href="#l309"></a>
<span id="l310">            <span class="n">k</span> <span class="o">=</span> <span class="n">m</span><span class="o">.</span><span class="n">end</span><span class="p">()</span></span><a href="#l310"></a>
<span id="l311"></span><a href="#l311"></a>
<span id="l312">        <span class="n">end</span> <span class="o">=</span> <span class="n">rawdata</span><span class="p">[</span><span class="n">k</span><span class="p">:</span><span class="n">endpos</span><span class="p">]</span><span class="o">.</span><span class="n">strip</span><span class="p">()</span></span><a href="#l312"></a>
<span id="l313">        <span class="k">if</span> <span class="n">end</span> <span class="ow">not</span> <span class="ow">in</span> <span class="p">(</span><span class="s">&quot;&gt;&quot;</span><span class="p">,</span> <span class="s">&quot;/&gt;&quot;</span><span class="p">):</span></span><a href="#l313"></a>
<span id="l314">            <span class="n">lineno</span><span class="p">,</span> <span class="n">offset</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">getpos</span><span class="p">()</span></span><a href="#l314"></a>
<span id="l315">            <span class="k">if</span> <span class="s">&quot;</span><span class="se">\n</span><span class="s">&quot;</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">__starttag_text</span><span class="p">:</span></span><a href="#l315"></a>
<span id="l316">                <span class="n">lineno</span> <span class="o">=</span> <span class="n">lineno</span> <span class="o">+</span> <span class="bp">self</span><span class="o">.</span><span class="n">__starttag_text</span><span class="o">.</span><span class="n">count</span><span class="p">(</span><span class="s">&quot;</span><span class="se">\n</span><span class="s">&quot;</span><span class="p">)</span></span><a href="#l316"></a>
<span id="l317">                <span class="n">offset</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">__starttag_text</span><span class="p">)</span> \</span><a href="#l317"></a>
<span id="l318">                         <span class="o">-</span> <span class="bp">self</span><span class="o">.</span><span class="n">__starttag_text</span><span class="o">.</span><span class="n">rfind</span><span class="p">(</span><span class="s">&quot;</span><span class="se">\n</span><span class="s">&quot;</span><span class="p">)</span></span><a href="#l318"></a>
<span id="l319">            <span class="k">else</span><span class="p">:</span></span><a href="#l319"></a>
<span id="l320">                <span class="n">offset</span> <span class="o">=</span> <span class="n">offset</span> <span class="o">+</span> <span class="nb">len</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">__starttag_text</span><span class="p">)</span></span><a href="#l320"></a>
<span id="l321">            <span class="bp">self</span><span class="o">.</span><span class="n">handle_data</span><span class="p">(</span><span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">endpos</span><span class="p">])</span></span><a href="#l321"></a>
<span id="l322">            <span class="k">return</span> <span class="n">endpos</span></span><a href="#l322"></a>
<span id="l323">        <span class="k">if</span> <span class="n">end</span><span class="o">.</span><span class="n">endswith</span><span class="p">(</span><span class="s">&#39;/&gt;&#39;</span><span class="p">):</span></span><a href="#l323"></a>
<span id="l324">            <span class="c"># XHTML-style empty tag: &lt;span attr=&quot;value&quot; /&gt;</span></span><a href="#l324"></a>
<span id="l325">            <span class="bp">self</span><span class="o">.</span><span class="n">handle_startendtag</span><span class="p">(</span><span class="n">tag</span><span class="p">,</span> <span class="n">attrs</span><span class="p">)</span></span><a href="#l325"></a>
<span id="l326">        <span class="k">else</span><span class="p">:</span></span><a href="#l326"></a>
<span id="l327">            <span class="bp">self</span><span class="o">.</span><span class="n">handle_starttag</span><span class="p">(</span><span class="n">tag</span><span class="p">,</span> <span class="n">attrs</span><span class="p">)</span></span><a href="#l327"></a>
<span id="l328">            <span class="k">if</span> <span class="n">tag</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">CDATA_CONTENT_ELEMENTS</span><span class="p">:</span></span><a href="#l328"></a>
<span id="l329">                <span class="bp">self</span><span class="o">.</span><span class="n">set_cdata_mode</span><span class="p">(</span><span class="n">tag</span><span class="p">)</span></span><a href="#l329"></a>
<span id="l330">        <span class="k">return</span> <span class="n">endpos</span></span><a href="#l330"></a>
<span id="l331"></span><a href="#l331"></a>
<span id="l332">    <span class="c"># Internal -- check to see if we have a complete starttag; return end</span></span><a href="#l332"></a>
<span id="l333">    <span class="c"># or -1 if incomplete.</span></span><a href="#l333"></a>
<span id="l334">    <span class="k">def</span> <span class="nf">check_for_whole_start_tag</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span></span><a href="#l334"></a>
<span id="l335">        <span class="n">rawdata</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">rawdata</span></span><a href="#l335"></a>
<span id="l336">        <span class="n">m</span> <span class="o">=</span> <span class="n">locatestarttagend</span><span class="o">.</span><span class="n">match</span><span class="p">(</span><span class="n">rawdata</span><span class="p">,</span> <span class="n">i</span><span class="p">)</span></span><a href="#l336"></a>
<span id="l337">        <span class="k">if</span> <span class="n">m</span><span class="p">:</span></span><a href="#l337"></a>
<span id="l338">            <span class="n">j</span> <span class="o">=</span> <span class="n">m</span><span class="o">.</span><span class="n">end</span><span class="p">()</span></span><a href="#l338"></a>
<span id="l339">            <span class="nb">next</span> <span class="o">=</span> <span class="n">rawdata</span><span class="p">[</span><span class="n">j</span><span class="p">:</span><span class="n">j</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span></span><a href="#l339"></a>
<span id="l340">            <span class="k">if</span> <span class="nb">next</span> <span class="o">==</span> <span class="s">&quot;&gt;&quot;</span><span class="p">:</span></span><a href="#l340"></a>
<span id="l341">                <span class="k">return</span> <span class="n">j</span> <span class="o">+</span> <span class="mi">1</span></span><a href="#l341"></a>
<span id="l342">            <span class="k">if</span> <span class="nb">next</span> <span class="o">==</span> <span class="s">&quot;/&quot;</span><span class="p">:</span></span><a href="#l342"></a>
<span id="l343">                <span class="k">if</span> <span class="n">rawdata</span><span class="o">.</span><span class="n">startswith</span><span class="p">(</span><span class="s">&quot;/&gt;&quot;</span><span class="p">,</span> <span class="n">j</span><span class="p">):</span></span><a href="#l343"></a>
<span id="l344">                    <span class="k">return</span> <span class="n">j</span> <span class="o">+</span> <span class="mi">2</span></span><a href="#l344"></a>
<span id="l345">                <span class="k">if</span> <span class="n">rawdata</span><span class="o">.</span><span class="n">startswith</span><span class="p">(</span><span class="s">&quot;/&quot;</span><span class="p">,</span> <span class="n">j</span><span class="p">):</span></span><a href="#l345"></a>
<span id="l346">                    <span class="c"># buffer boundary</span></span><a href="#l346"></a>
<span id="l347">                    <span class="k">return</span> <span class="o">-</span><span class="mi">1</span></span><a href="#l347"></a>
<span id="l348">                <span class="c"># else bogus input</span></span><a href="#l348"></a>
<span id="l349">                <span class="bp">self</span><span class="o">.</span><span class="n">updatepos</span><span class="p">(</span><span class="n">i</span><span class="p">,</span> <span class="n">j</span> <span class="o">+</span> <span class="mi">1</span><span class="p">)</span></span><a href="#l349"></a>
<span id="l350">                <span class="bp">self</span><span class="o">.</span><span class="n">error</span><span class="p">(</span><span class="s">&quot;malformed empty start tag&quot;</span><span class="p">)</span></span><a href="#l350"></a>
<span id="l351">            <span class="k">if</span> <span class="nb">next</span> <span class="o">==</span> <span class="s">&quot;&quot;</span><span class="p">:</span></span><a href="#l351"></a>
<span id="l352">                <span class="c"># end of input</span></span><a href="#l352"></a>
<span id="l353">                <span class="k">return</span> <span class="o">-</span><span class="mi">1</span></span><a href="#l353"></a>
<span id="l354">            <span class="k">if</span> <span class="nb">next</span> <span class="ow">in</span> <span class="p">(</span><span class="s">&quot;abcdefghijklmnopqrstuvwxyz=/&quot;</span></span><a href="#l354"></a>
<span id="l355">                        <span class="s">&quot;ABCDEFGHIJKLMNOPQRSTUVWXYZ&quot;</span><span class="p">):</span></span><a href="#l355"></a>
<span id="l356">                <span class="c"># end of input in or before attribute value, or we have the</span></span><a href="#l356"></a>
<span id="l357">                <span class="c"># &#39;/&#39; from a &#39;/&gt;&#39; ending</span></span><a href="#l357"></a>
<span id="l358">                <span class="k">return</span> <span class="o">-</span><span class="mi">1</span></span><a href="#l358"></a>
<span id="l359">            <span class="k">if</span> <span class="n">j</span> <span class="o">&gt;</span> <span class="n">i</span><span class="p">:</span></span><a href="#l359"></a>
<span id="l360">                <span class="k">return</span> <span class="n">j</span></span><a href="#l360"></a>
<span id="l361">            <span class="k">else</span><span class="p">:</span></span><a href="#l361"></a>
<span id="l362">                <span class="k">return</span> <span class="n">i</span> <span class="o">+</span> <span class="mi">1</span></span><a href="#l362"></a>
<span id="l363">        <span class="k">raise</span> <span class="ne">AssertionError</span><span class="p">(</span><span class="s">&quot;we should not get here!&quot;</span><span class="p">)</span></span><a href="#l363"></a>
<span id="l364"></span><a href="#l364"></a>
<span id="l365">    <span class="c"># Internal -- parse endtag, return end or -1 if incomplete</span></span><a href="#l365"></a>
<span id="l366">    <span class="k">def</span> <span class="nf">parse_endtag</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span></span><a href="#l366"></a>
<span id="l367">        <span class="n">rawdata</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">rawdata</span></span><a href="#l367"></a>
<span id="l368">        <span class="k">assert</span> <span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">i</span><span class="o">+</span><span class="mi">2</span><span class="p">]</span> <span class="o">==</span> <span class="s">&quot;&lt;/&quot;</span><span class="p">,</span> <span class="s">&quot;unexpected call to parse_endtag&quot;</span></span><a href="#l368"></a>
<span id="l369">        <span class="n">match</span> <span class="o">=</span> <span class="n">endendtag</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">rawdata</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">)</span> <span class="c"># &gt;</span></span><a href="#l369"></a>
<span id="l370">        <span class="k">if</span> <span class="ow">not</span> <span class="n">match</span><span class="p">:</span></span><a href="#l370"></a>
<span id="l371">            <span class="k">return</span> <span class="o">-</span><span class="mi">1</span></span><a href="#l371"></a>
<span id="l372">        <span class="n">gtpos</span> <span class="o">=</span> <span class="n">match</span><span class="o">.</span><span class="n">end</span><span class="p">()</span></span><a href="#l372"></a>
<span id="l373">        <span class="n">match</span> <span class="o">=</span> <span class="n">endtagfind</span><span class="o">.</span><span class="n">match</span><span class="p">(</span><span class="n">rawdata</span><span class="p">,</span> <span class="n">i</span><span class="p">)</span> <span class="c"># &lt;/ + tag + &gt;</span></span><a href="#l373"></a>
<span id="l374">        <span class="k">if</span> <span class="ow">not</span> <span class="n">match</span><span class="p">:</span></span><a href="#l374"></a>
<span id="l375">            <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">cdata_elem</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l375"></a>
<span id="l376">                <span class="bp">self</span><span class="o">.</span><span class="n">handle_data</span><span class="p">(</span><span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">gtpos</span><span class="p">])</span></span><a href="#l376"></a>
<span id="l377">                <span class="k">return</span> <span class="n">gtpos</span></span><a href="#l377"></a>
<span id="l378">            <span class="c"># find the name: w3.org/TR/html5/tokenization.html#tag-name-state</span></span><a href="#l378"></a>
<span id="l379">            <span class="n">namematch</span> <span class="o">=</span> <span class="n">tagfind</span><span class="o">.</span><span class="n">match</span><span class="p">(</span><span class="n">rawdata</span><span class="p">,</span> <span class="n">i</span><span class="o">+</span><span class="mi">2</span><span class="p">)</span></span><a href="#l379"></a>
<span id="l380">            <span class="k">if</span> <span class="ow">not</span> <span class="n">namematch</span><span class="p">:</span></span><a href="#l380"></a>
<span id="l381">                <span class="c"># w3.org/TR/html5/tokenization.html#end-tag-open-state</span></span><a href="#l381"></a>
<span id="l382">                <span class="k">if</span> <span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">i</span><span class="o">+</span><span class="mi">3</span><span class="p">]</span> <span class="o">==</span> <span class="s">&#39;&lt;/&gt;&#39;</span><span class="p">:</span></span><a href="#l382"></a>
<span id="l383">                    <span class="k">return</span> <span class="n">i</span><span class="o">+</span><span class="mi">3</span></span><a href="#l383"></a>
<span id="l384">                <span class="k">else</span><span class="p">:</span></span><a href="#l384"></a>
<span id="l385">                    <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">parse_bogus_comment</span><span class="p">(</span><span class="n">i</span><span class="p">)</span></span><a href="#l385"></a>
<span id="l386">            <span class="n">tagname</span> <span class="o">=</span> <span class="n">namematch</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span></span><a href="#l386"></a>
<span id="l387">            <span class="c"># consume and ignore other stuff between the name and the &gt;</span></span><a href="#l387"></a>
<span id="l388">            <span class="c"># Note: this is not 100% correct, since we might have things like</span></span><a href="#l388"></a>
<span id="l389">            <span class="c"># &lt;/tag attr=&quot;&gt;&quot;&gt;, but looking for &gt; after tha name should cover</span></span><a href="#l389"></a>
<span id="l390">            <span class="c"># most of the cases and is much simpler</span></span><a href="#l390"></a>
<span id="l391">            <span class="n">gtpos</span> <span class="o">=</span> <span class="n">rawdata</span><span class="o">.</span><span class="n">find</span><span class="p">(</span><span class="s">&#39;&gt;&#39;</span><span class="p">,</span> <span class="n">namematch</span><span class="o">.</span><span class="n">end</span><span class="p">())</span></span><a href="#l391"></a>
<span id="l392">            <span class="bp">self</span><span class="o">.</span><span class="n">handle_endtag</span><span class="p">(</span><span class="n">tagname</span><span class="p">)</span></span><a href="#l392"></a>
<span id="l393">            <span class="k">return</span> <span class="n">gtpos</span><span class="o">+</span><span class="mi">1</span></span><a href="#l393"></a>
<span id="l394"></span><a href="#l394"></a>
<span id="l395">        <span class="n">elem</span> <span class="o">=</span> <span class="n">match</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span> <span class="c"># script or style</span></span><a href="#l395"></a>
<span id="l396">        <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">cdata_elem</span> <span class="ow">is</span> <span class="ow">not</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l396"></a>
<span id="l397">            <span class="k">if</span> <span class="n">elem</span> <span class="o">!=</span> <span class="bp">self</span><span class="o">.</span><span class="n">cdata_elem</span><span class="p">:</span></span><a href="#l397"></a>
<span id="l398">                <span class="bp">self</span><span class="o">.</span><span class="n">handle_data</span><span class="p">(</span><span class="n">rawdata</span><span class="p">[</span><span class="n">i</span><span class="p">:</span><span class="n">gtpos</span><span class="p">])</span></span><a href="#l398"></a>
<span id="l399">                <span class="k">return</span> <span class="n">gtpos</span></span><a href="#l399"></a>
<span id="l400"></span><a href="#l400"></a>
<span id="l401">        <span class="bp">self</span><span class="o">.</span><span class="n">handle_endtag</span><span class="p">(</span><span class="n">elem</span><span class="p">)</span></span><a href="#l401"></a>
<span id="l402">        <span class="bp">self</span><span class="o">.</span><span class="n">clear_cdata_mode</span><span class="p">()</span></span><a href="#l402"></a>
<span id="l403">        <span class="k">return</span> <span class="n">gtpos</span></span><a href="#l403"></a>
<span id="l404"></span><a href="#l404"></a>
<span id="l405">    <span class="c"># Overridable -- finish processing of start+end tag: &lt;tag.../&gt;</span></span><a href="#l405"></a>
<span id="l406">    <span class="k">def</span> <span class="nf">handle_startendtag</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">tag</span><span class="p">,</span> <span class="n">attrs</span><span class="p">):</span></span><a href="#l406"></a>
<span id="l407">        <span class="bp">self</span><span class="o">.</span><span class="n">handle_starttag</span><span class="p">(</span><span class="n">tag</span><span class="p">,</span> <span class="n">attrs</span><span class="p">)</span></span><a href="#l407"></a>
<span id="l408">        <span class="bp">self</span><span class="o">.</span><span class="n">handle_endtag</span><span class="p">(</span><span class="n">tag</span><span class="p">)</span></span><a href="#l408"></a>
<span id="l409"></span><a href="#l409"></a>
<span id="l410">    <span class="c"># Overridable -- handle start tag</span></span><a href="#l410"></a>
<span id="l411">    <span class="k">def</span> <span class="nf">handle_starttag</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">tag</span><span class="p">,</span> <span class="n">attrs</span><span class="p">):</span></span><a href="#l411"></a>
<span id="l412">        <span class="k">pass</span></span><a href="#l412"></a>
<span id="l413"></span><a href="#l413"></a>
<span id="l414">    <span class="c"># Overridable -- handle end tag</span></span><a href="#l414"></a>
<span id="l415">    <span class="k">def</span> <span class="nf">handle_endtag</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">tag</span><span class="p">):</span></span><a href="#l415"></a>
<span id="l416">        <span class="k">pass</span></span><a href="#l416"></a>
<span id="l417"></span><a href="#l417"></a>
<span id="l418">    <span class="c"># Overridable -- handle character reference</span></span><a href="#l418"></a>
<span id="l419">    <span class="k">def</span> <span class="nf">handle_charref</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">):</span></span><a href="#l419"></a>
<span id="l420">        <span class="k">pass</span></span><a href="#l420"></a>
<span id="l421"></span><a href="#l421"></a>
<span id="l422">    <span class="c"># Overridable -- handle entity reference</span></span><a href="#l422"></a>
<span id="l423">    <span class="k">def</span> <span class="nf">handle_entityref</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">):</span></span><a href="#l423"></a>
<span id="l424">        <span class="k">pass</span></span><a href="#l424"></a>
<span id="l425"></span><a href="#l425"></a>
<span id="l426">    <span class="c"># Overridable -- handle data</span></span><a href="#l426"></a>
<span id="l427">    <span class="k">def</span> <span class="nf">handle_data</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">):</span></span><a href="#l427"></a>
<span id="l428">        <span class="k">pass</span></span><a href="#l428"></a>
<span id="l429"></span><a href="#l429"></a>
<span id="l430">    <span class="c"># Overridable -- handle comment</span></span><a href="#l430"></a>
<span id="l431">    <span class="k">def</span> <span class="nf">handle_comment</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">):</span></span><a href="#l431"></a>
<span id="l432">        <span class="k">pass</span></span><a href="#l432"></a>
<span id="l433"></span><a href="#l433"></a>
<span id="l434">    <span class="c"># Overridable -- handle declaration</span></span><a href="#l434"></a>
<span id="l435">    <span class="k">def</span> <span class="nf">handle_decl</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">decl</span><span class="p">):</span></span><a href="#l435"></a>
<span id="l436">        <span class="k">pass</span></span><a href="#l436"></a>
<span id="l437"></span><a href="#l437"></a>
<span id="l438">    <span class="c"># Overridable -- handle processing instruction</span></span><a href="#l438"></a>
<span id="l439">    <span class="k">def</span> <span class="nf">handle_pi</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">):</span></span><a href="#l439"></a>
<span id="l440">        <span class="k">pass</span></span><a href="#l440"></a>
<span id="l441"></span><a href="#l441"></a>
<span id="l442">    <span class="k">def</span> <span class="nf">unknown_decl</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">):</span></span><a href="#l442"></a>
<span id="l443">        <span class="k">pass</span></span><a href="#l443"></a>
<span id="l444"></span><a href="#l444"></a>
<span id="l445">    <span class="c"># Internal -- helper to remove special character quoting</span></span><a href="#l445"></a>
<span id="l446">    <span class="n">entitydefs</span> <span class="o">=</span> <span class="bp">None</span></span><a href="#l446"></a>
<span id="l447">    <span class="k">def</span> <span class="nf">unescape</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">s</span><span class="p">):</span></span><a href="#l447"></a>
<span id="l448">        <span class="k">if</span> <span class="s">&#39;&amp;&#39;</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">s</span><span class="p">:</span></span><a href="#l448"></a>
<span id="l449">            <span class="k">return</span> <span class="n">s</span></span><a href="#l449"></a>
<span id="l450">        <span class="k">def</span> <span class="nf">replaceEntities</span><span class="p">(</span><span class="n">s</span><span class="p">):</span></span><a href="#l450"></a>
<span id="l451">            <span class="n">s</span> <span class="o">=</span> <span class="n">s</span><span class="o">.</span><span class="n">groups</span><span class="p">()[</span><span class="mi">0</span><span class="p">]</span></span><a href="#l451"></a>
<span id="l452">            <span class="k">try</span><span class="p">:</span></span><a href="#l452"></a>
<span id="l453">                <span class="k">if</span> <span class="n">s</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">==</span> <span class="s">&quot;#&quot;</span><span class="p">:</span></span><a href="#l453"></a>
<span id="l454">                    <span class="n">s</span> <span class="o">=</span> <span class="n">s</span><span class="p">[</span><span class="mi">1</span><span class="p">:]</span></span><a href="#l454"></a>
<span id="l455">                    <span class="k">if</span> <span class="n">s</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="ow">in</span> <span class="p">[</span><span class="s">&#39;x&#39;</span><span class="p">,</span><span class="s">&#39;X&#39;</span><span class="p">]:</span></span><a href="#l455"></a>
<span id="l456">                        <span class="n">c</span> <span class="o">=</span> <span class="nb">int</span><span class="p">(</span><span class="n">s</span><span class="p">[</span><span class="mi">1</span><span class="p">:],</span> <span class="mi">16</span><span class="p">)</span></span><a href="#l456"></a>
<span id="l457">                    <span class="k">else</span><span class="p">:</span></span><a href="#l457"></a>
<span id="l458">                        <span class="n">c</span> <span class="o">=</span> <span class="nb">int</span><span class="p">(</span><span class="n">s</span><span class="p">)</span></span><a href="#l458"></a>
<span id="l459">                    <span class="k">return</span> <span class="nb">unichr</span><span class="p">(</span><span class="n">c</span><span class="p">)</span></span><a href="#l459"></a>
<span id="l460">            <span class="k">except</span> <span class="ne">ValueError</span><span class="p">:</span></span><a href="#l460"></a>
<span id="l461">                <span class="k">return</span> <span class="s">&#39;&amp;#&#39;</span><span class="o">+</span><span class="n">s</span><span class="o">+</span><span class="s">&#39;;&#39;</span></span><a href="#l461"></a>
<span id="l462">            <span class="k">else</span><span class="p">:</span></span><a href="#l462"></a>
<span id="l463">                <span class="c"># Cannot use name2codepoint directly, because HTMLParser supports apos,</span></span><a href="#l463"></a>
<span id="l464">                <span class="c"># which is not part of HTML 4</span></span><a href="#l464"></a>
<span id="l465">                <span class="kn">import</span> <span class="nn">htmlentitydefs</span></span><a href="#l465"></a>
<span id="l466">                <span class="k">if</span> <span class="n">HTMLParser</span><span class="o">.</span><span class="n">entitydefs</span> <span class="ow">is</span> <span class="bp">None</span><span class="p">:</span></span><a href="#l466"></a>
<span id="l467">                    <span class="n">entitydefs</span> <span class="o">=</span> <span class="n">HTMLParser</span><span class="o">.</span><span class="n">entitydefs</span> <span class="o">=</span> <span class="p">{</span><span class="s">&#39;apos&#39;</span><span class="p">:</span><span class="s">u&quot;&#39;&quot;</span><span class="p">}</span></span><a href="#l467"></a>
<span id="l468">                    <span class="k">for</span> <span class="n">k</span><span class="p">,</span> <span class="n">v</span> <span class="ow">in</span> <span class="n">htmlentitydefs</span><span class="o">.</span><span class="n">name2codepoint</span><span class="o">.</span><span class="n">iteritems</span><span class="p">():</span></span><a href="#l468"></a>
<span id="l469">                        <span class="n">entitydefs</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="nb">unichr</span><span class="p">(</span><span class="n">v</span><span class="p">)</span></span><a href="#l469"></a>
<span id="l470">                <span class="k">try</span><span class="p">:</span></span><a href="#l470"></a>
<span id="l471">                    <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">entitydefs</span><span class="p">[</span><span class="n">s</span><span class="p">]</span></span><a href="#l471"></a>
<span id="l472">                <span class="k">except</span> <span class="ne">KeyError</span><span class="p">:</span></span><a href="#l472"></a>
<span id="l473">                    <span class="k">return</span> <span class="s">&#39;&amp;&#39;</span><span class="o">+</span><span class="n">s</span><span class="o">+</span><span class="s">&#39;;&#39;</span></span><a href="#l473"></a>
<span id="l474"></span><a href="#l474"></a>
<span id="l475">        <span class="k">return</span> <span class="n">re</span><span class="o">.</span><span class="n">sub</span><span class="p">(</span><span class="s">r&quot;&amp;(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));&quot;</span><span class="p">,</span> <span class="n">replaceEntities</span><span class="p">,</span> <span class="n">s</span><span class="p">)</span></span><a href="#l475"></a></pre>
<div class="sourcelast"></div>
</div>
</div>
</div>

<script type="text/javascript">process_dates()</script>


</body>
</html>

