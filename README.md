





<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
  <link rel="dns-prefetch" href="https://assets-cdn.github.com">
  <link rel="dns-prefetch" href="https://avatars0.githubusercontent.com">
  <link rel="dns-prefetch" href="https://avatars1.githubusercontent.com">
  <link rel="dns-prefetch" href="https://avatars2.githubusercontent.com">
  <link rel="dns-prefetch" href="https://avatars3.githubusercontent.com">
  <link rel="dns-prefetch" href="https://github-cloud.s3.amazonaws.com">
  <link rel="dns-prefetch" href="https://user-images.githubusercontent.com/">


    
  <div id="readme" class="readme blob instapaper_body">
    <article class="markdown-body entry-content" itemprop="text"><h1><a id="user-content-colorcoderescaling" class="anchor" aria-hidden="true" href="#colorcoderescaling"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>colorCodeRescaling</h1>
<p>Decoder for the color code based on rescaling of the lattice</p>
<p>Content:</p>
<pre><code>          colorCodeh.py
</code></pre>
<p>it is the core of the program. Contains the classes Cell and ColorCode, and a lookuptable function for the 1 qubit cell.</p>
<pre><code>The lookuptable function works for cells of 4 qubits and 3 stabilizers. The lookuptable has been introduced
</code></pre>
<p>entirely by hand. The indexes have been introduced according to the notes. They should have the same notation as
the Cell class.</p>
<pre><code>The class Cell is an utility for the main class ColorCode. It contains for each cell, the information about 
</code></pre>
<p>the indexes correspondent to the qubits and syndromes in the full code:</p>
<p>Cell[i].q=[q0,q1,q2,q3] contains the indexes(with respecto to the full code) of the four qubits inside cell i;
Cell[i].s=[s0,s1,s2] contains the indexes of the 3 syndromes in the boundaries</p>
<p>in this way, the main code can simply call the decoder of a cell, and it will look for the appropiate values of the probabilities
of error in single qubits, and the appropiate values for the syndromes s0,s1,s2, so that it can check the lookuptable.</p>
<pre><code>The class ColorCode contains all the variables and functions needed for a simulation. The main functions in the code are
</code></pre>
<p>the one for plotting, and the one for decoding an entire code, together with the one for generating noise and measure the
syndrome. So here is a brief explanation:</p>
<p>ColorCode(m,p) generates the data structure. The number of qubits is 18·2^(2m), and the probability of error of each
qubit is set to p. The initialization process also creates variables in which to store the error configuration, the syndrome, the
correction, and the splittings.</p>
<p>noise() generates X errors in the qubits with probability p. The value of p is set in the initialization of the class.</p>
<p>syndrome() measures the syndrome that corresponds to the actual error configuration.</p>
<p>hardDecoder(softsplit=True,plotall=False) generates a correction according to the measured syndrome.The variables of
the input allow to choose between the soft-hard splitting methods, and to plot the intermediate steps. The function
stores the correction information in the internal variable for the correction values. The way the
decoder works is the following:
0. If the code has size m=0, applies the lookuptable decoder for 18 qubits, otherwise:</p>
<pre><code>  1. Applies the resplitting function (soft or hard) until convergence, or until 45 resplitting steps (first to happen).
  2. Decodes each of the cells using the lookuptable for 4 qubits.
  3. Creates a new code, with size m-1, and initializes it with the values of the corner syndromes (after applying the
    corrections from the cells to the measurements of those syndromes), and with the new probabilities of error 
    of the qubits according to the probability of logical error of each cell.
    
  4. Applies the function code.hardDecoder() of the new code. That means this process is applied recursively unitl the
    new code has size m=0, in which case the process finishes.
  5. Translates the corrections in the higher levels of encoding to the lower levels, by applying the logical operator
    of the cells in which there is a correction.
</code></pre>
<p>plot(lattice=True,qubits=False,syndrome=True,correction=True, cells=False, error=True, splitting=False,coll='k')
This functions plots the lattice. The variables in the input are there to activate the plotting of:</p>
<pre><code>  lattice: the lattice of the code, basic for everything.
  qubits: it plots a q over every qubit. It is just for debugging.
  syndrome: the values of the measurements of the syndromes. Plots a yellow ball over the -1 syndromes.
  correction: plots a C over the qubits with a correction.
  cells: plots the cells by writing the word CELL over every qubit in a cell, with a different colour per cell.
  error: plots an X over the qubits with error.
  splitting: plots the current splitting, (u for split[i]=0, d otherwise, and a + or - sign for each of the half splits)
  coll: is the colour used to plot the lattice.
</code></pre>
<p>the rest of the functions are mostly for the decoder to work. That includes the soft and hard splitting functions,
several functions to compute probabilities of splittings, and the decoder for the 18 qubit case. Apart from those,
there are other functions made for the debugging and for the testing of the algorithms:</p>
<pre><code>energy(): measures the value of the "energy" of the current splitting, by computing the minus logarithm of the sum
  of the probabilities of the possible error configurations inside the cells assuming the current splitting.
  
fullsplittester(printon=False): this functions computes the energy of each and every possible splitting, and returns
  the minimum of that energy, and the corresponding splitting. The input variable printon makes it print the progress
  of the program (as it takes very long for codes of the size of m=1). 
</code></pre>
</article>
  </div>

  </div>

  <button type="button" data-facebox="#jump-to-line" data-facebox-class="linejump" data-hotkey="l" class="d-none">Jump to Line</button>
  <div id="jump-to-line" style="display:none">
    <!-- '"` --><!-- </textarea></xmp> --></option></form><form class="js-jump-to-line-form" action="" accept-charset="UTF-8" method="get"><input name="utf8" type="hidden" value="&#x2713;" />
      <input class="form-control linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" aria-label="Jump to line" autofocus>
      <button type="submit" class="btn">Go</button>
</form>  </div>


  </div>
  <div class="modal-backdrop js-touch-events"></div>
</div>

    </div>
  </div>

  </div>

      
<div class="footer container-lg px-3" role="contentinfo">
  <div class="position-relative d-flex flex-justify-between py-6 mt-6 f6 text-gray border-top border-gray-light ">
    <ul class="list-style-none d-flex flex-wrap ">
      <li class="mr-3">&copy; 2018 <span title="0.29018s from unicorn-2648019222-2w251">GitHub</span>, Inc.</li>
        <li class="mr-3"><a href="https://help.github.com/articles/github-terms-of-service/" data-ga-click="Footer, go to terms, text:terms">Terms</a></li>
        <li class="mr-3"><a href="https://github.com/site/privacy" data-ga-click="Footer, go to privacy, text:privacy">Privacy</a></li>
        <li class="mr-3"><a href="https://help.github.com/articles/github-security/" data-ga-click="Footer, go to security, text:security">Security</a></li>
        <li class="mr-3"><a href="https://status.github.com/" data-ga-click="Footer, go to status, text:status">Status</a></li>
        <li><a data-ga-click="Footer, go to help, text:help" href="https://help.github.com">Help</a></li>
    </ul>

    <a aria-label="Homepage" title="GitHub" class="footer-octicon" href="https://github.com">
      <svg height="24" class="octicon octicon-mark-github" viewBox="0 0 16 16" version="1.1" width="24" aria-hidden="true"><path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>
</a>
    <ul class="list-style-none d-flex flex-wrap ">
        <li class="mr-3"><a data-ga-click="Footer, go to contact, text:contact" href="https://github.com/contact">Contact GitHub</a></li>
      <li class="mr-3"><a href="https://developer.github.com" data-ga-click="Footer, go to api, text:api">API</a></li>
      <li class="mr-3"><a href="https://training.github.com" data-ga-click="Footer, go to training, text:training">Training</a></li>
      <li class="mr-3"><a href="https://shop.github.com" data-ga-click="Footer, go to shop, text:shop">Shop</a></li>
        <li class="mr-3"><a data-ga-click="Footer, go to blog, text:blog" href="https://github.com/blog">Blog</a></li>
        <li><a data-ga-click="Footer, go to about, text:about" href="https://github.com/about">About</a></li>

    </ul>
  </div>
</div>



  <div id="ajax-error-message" class="ajax-error-message flash flash-error">
    <svg class="octicon octicon-alert" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M8.865 1.52c-.18-.31-.51-.5-.87-.5s-.69.19-.87.5L.275 13.5c-.18.31-.18.69 0 1 .19.31.52.5.87.5h13.7c.36 0 .69-.19.86-.5.17-.31.18-.69.01-1L8.865 1.52zM8.995 13h-2v-2h2v2zm0-3h-2V6h2v4z"/></svg>
    <button type="button" class="flash-close js-ajax-error-dismiss" aria-label="Dismiss error">
      <svg class="octicon octicon-x" viewBox="0 0 12 16" version="1.1" width="12" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.48 8l3.75 3.75-1.48 1.48L6 9.48l-3.75 3.75-1.48-1.48L4.52 8 .77 4.25l1.48-1.48L6 6.52l3.75-3.75 1.48 1.48z"/></svg>
    </button>
    You can't perform that action at this time.
  </div>


    
    <script crossorigin="anonymous" integrity="sha512-opnS0aay2ZbyHDGGXD1rqjVRR+MVTaj7nr5X1kI7LNiySlgjwWgPt1lL175Qrd6U3AV2iZdYBqOLcTW1eKgHQw==" type="application/javascript" src="https://assets-cdn.github.com/assets/frameworks-5666c84bff85.js"></script>
    
    <script crossorigin="anonymous" async="async" integrity="sha512-lcdjGsOZ0NIwSLFlj3y70wlBWOizB0Gx8R+47wY5Nwuus+dIQccI6Cl7epc+bZnsUzFbt6ERcyJSX5tK9Km4fg==" type="application/javascript" src="https://assets-cdn.github.com/assets/github-ad12aa3f169e.js"></script>
    
    
    
    
  <div class="js-stale-session-flash stale-session-flash flash flash-warn flash-banner d-none">
    <svg class="octicon octicon-alert" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M8.865 1.52c-.18-.31-.51-.5-.87-.5s-.69.19-.87.5L.275 13.5c-.18.31-.18.69 0 1 .19.31.52.5.87.5h13.7c.36 0 .69-.19.86-.5.17-.31.18-.69.01-1L8.865 1.52zM8.995 13h-2v-2h2v2zm0-3h-2V6h2v4z"/></svg>
    <span class="signed-in-tab-flash">You signed in with another tab or window. <a href="">Reload</a> to refresh your session.</span>
    <span class="signed-out-tab-flash">You signed out in another tab or window. <a href="">Reload</a> to refresh your session.</span>
  </div>
  <div class="facebox" id="facebox" style="display:none;">
  <div class="facebox-popup">
    <div class="facebox-content" role="dialog" aria-labelledby="facebox-header" aria-describedby="facebox-description">
    </div>
    <button type="button" class="facebox-close js-facebox-close" aria-label="Close modal">
      <svg class="octicon octicon-x" viewBox="0 0 12 16" version="1.1" width="12" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.48 8l3.75 3.75-1.48 1.48L6 9.48l-3.75 3.75-1.48-1.48L4.52 8 .77 4.25l1.48-1.48L6 6.52l3.75-3.75 1.48 1.48z"/></svg>
    </button>
  </div>
</div>

  

  </body>
</html>

