// ==UserScript==
// @name    SRA-Galaxy  
// @namespace   http://mattshirley.com  
// @include http://trace.ncbi.nlm.nih.gov/Traces/sra/*
// @run-at      document-start
// @grant       GM_addStyle
// ==/UserScript==
function contentEval(source) {
  // Check for function input.
  if ('function' == typeof source) {
    // Execute this function with no arguments, by adding parentheses.
    // One set around the function, required for valid syntax, and a
    // second empty set calls the surrounded function.
    source = '(' + source + ')();'
  }

  // Create a script node holding this  source code.
  var script = document.createElement('script');
  script.setAttribute("type", "application/javascript");
  script.textContent = source;

  // Insert the script node into the page, so it will run, and immediately
  // remove it to clean up.
  document.body.appendChild(script);
  document.body.removeChild(script);
}

function setCookie(c_name,value,exdays)
{
var exdate=new Date();
exdate.setDate(exdate.getDate() + exdays);
var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
document.cookie=c_name + "=" + c_value;
}

function getCookie(c_name)
{
var c_value = document.cookie;
var c_start = c_value.indexOf(" " + c_name + "=");
if (c_start == -1)
  {
  c_start = c_value.indexOf(c_name + "=");
  }
if (c_start == -1)
  {
  c_value = null;
  }
else
  {
  c_start = c_value.indexOf("=", c_start) + 1;
  var c_end = c_value.indexOf(";", c_start);
  if (c_end == -1)
  {
c_end = c_value.length;
}
c_value = unescape(c_value.substring(c_start,c_end));
}
return c_value;
}

function appendContentInNestedContainer(matchClass,content) {
    var elems = document.getElementsByTagName('*'), i;
    for (i in elems) {
        if((' ' + elems[i].className + ' ').indexOf(' ' + matchClass + ' ')
                > -1) {
            elems[i].firstChild.innerHTML = elems[i].firstChild.innerHTML + content;
        }
    }
}

// Read key value pairs so we can find Galaxy parameters to store
var $_GET = {};
document.location.search.replace(/\??(?:([^=]+)=([^&]*)&?)/g, function () {
    function decode(s) {
        return decodeURIComponent(s.split("+").join(" "));
    }

    $_GET[decode(arguments[1])] = decode(arguments[2]);
});
// Store Galaxy parameters for use in re-submission action
if ($_GET["GALAXY_URL"] != null) { setCookie("GALAXY_URL",$_GET["GALAXY_URL"],1); }
if ($_GET["tool_id"] != null) { setCookie("tool_id",$_GET["tool_id"],1); }
if ($_GET["sendToGalaxy"] != null) { setCookie("sendToGalaxy",$_GET["sendToGalaxy"],1); }



function submitToGalaxy() {
    function generateRequestURL() {
        frm = document.getElementById('alignment_form');
        path = frm.elements['path'].value;
        run = frm.elements['run'].value;
        acc = frm.elements['acc'].value;
        ref = frm.elements['ref'].value;
        range = frm.elements['range'].value;
        src = frm.elements['src'].value;
        output = frm.elements['output'].value;
        output_to = 'File';
        var URL="http://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?path=" + path + "&run=" + run + "&acc=" + acc + "&ref=" + ref + "&range=" + range + "&src=" + src + "&output=" + output + "&output_to=" + output_to;
        return URL;
    }
    var frm = document.getElementById('alignment_form') || null;
    if(frm) {
        URL = generateRequestURL();
        redirect = getCookie("GALAXY_URL") + "?tool_id=" + getCookie("tool_id") + "&URL=" + URL;
        window.location = redirect
    }
}

if (getCookie("sendToGalaxy") == 1) { 
    // Add "Galaxy" button to page    
    appendContentInNestedContainer('ph sample','<button id="sendToGalaxy" onclick="function() { var frm = document.getElementById('alignment_form'); var path = frm.elements['path'].value; var run = frm.elements['run'].value; var acc = frm.elements['acc'].value; var ref = frm.elements['ref'].value; var range = frm.elements['range'].value; var src = frm.elements['src'].value; var output = frm.elements['output'].value; var output_to = 'File'; var URL="http://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?path=" + path + '&run=' + run + '&acc=' + acc + '&ref=' + ref + '&range=' + range + '&src=' + src + '&output=' + output + '&output_to=' + output_to; var frm = document.getElementById('alignment_form') || null; if(frm) { URL = generateRequestURL(); redirect = getCookie('GALAXY_URL') + '?tool_id=' + getCookie('tool_id') + '&URL=' + URL; window.location = redirect; } }">Galaxy</button>'); 
}