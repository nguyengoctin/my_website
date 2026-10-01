(function() {
  function copyTextToClipboard(text, onSuccess, onError) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(onSuccess).catch(function() {
        fallbackCopy(text, onSuccess, onError);
      });
    } else {
      fallbackCopy(text, onSuccess, onError);
    }
  }

  function fallbackCopy(text, onSuccess, onError) {
    var textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    textarea.style.top = '0';
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    try {
      document.execCommand('copy');
      if (onSuccess) onSuccess();
    } catch (err) {
      console.error('Copy fallback failed', err);
      if (onError) onError(err);
    }
    document.body.removeChild(textarea);
  }

  document.addEventListener('click', function(e) {
    var codeBtn = e.target.closest('.code-block .copy');
    if (codeBtn) {
      e.preventDefault();
      e.stopPropagation();

      var codeBlock = codeBtn.closest('.code-block');
      if (!codeBlock) return;

      var codeText = '';
      var codeEl = codeBlock.querySelector('.highlight pre code') || codeBlock.querySelector('code');
      if (codeEl) {
        var lines = codeEl.querySelectorAll('span.line');
        if (lines && lines.length > 0) {
          var textArr = [];
          for (var i = 0; i < lines.length; i++) {
            textArr.push(lines[i].innerText.replace(/\r?\n$/, ''));
          }
          codeText = textArr.join('\n');
        } else {
          codeText = codeEl.innerText;
        }
      }
      if (!codeText) return;

      var copyIcon = codeBtn.querySelector('i');
      copyTextToClipboard(codeText, function() {
        codeBtn.classList.add('copied');
        if (copyIcon) copyIcon.className = 'ti ti-check fa-fw';
        setTimeout(function() {
          codeBtn.classList.remove('copied');
          if (copyIcon) copyIcon.className = 'ti ti-copy fa-fw';
        }, 2000);
      });
      return;
    }

    var mdBtn = e.target.closest('.btn-copy-markdown');
    if (mdBtn) {
      e.preventDefault();
      e.stopPropagation();

      var rawBase64 = mdBtn.getAttribute('data-markdown');
      if (!rawBase64) return;

      var markdownText = '';
      try {
        var binaryString = atob(rawBase64);
        var bytes = new Uint8Array(binaryString.length);
        for (var i = 0; i < binaryString.length; i++) {
          bytes[i] = binaryString.charCodeAt(i);
        }
        markdownText = new TextDecoder('utf-8').decode(bytes);
      } catch (err) {
        console.error('Base64 decode failed', err);
        return;
      }

      var mdIcon = mdBtn.querySelector('i');
      var mdTextSpan = mdBtn.querySelector('span');
      var origMdText = mdTextSpan ? mdTextSpan.textContent : '';

      copyTextToClipboard(markdownText, function() {
        mdBtn.classList.add('copied');
        if (mdIcon) mdIcon.className = 'ti ti-check';
        if (mdTextSpan) mdTextSpan.textContent = 'Copied!';
        setTimeout(function() {
          mdBtn.classList.remove('copied');
          if (mdIcon) mdIcon.className = 'ti ti-markdown';
          if (mdTextSpan) mdTextSpan.textContent = origMdText;
        }, 2000);
      });
      return;
    }

    var linkBtn = e.target.closest('.btn-copy-link');
    if (linkBtn) {
      e.preventDefault();
      e.stopPropagation();

      var url = linkBtn.getAttribute('data-url') || window.location.href;
      var linkIcon = linkBtn.querySelector('i');
      var linkTextSpan = linkBtn.querySelector('.copy-text') || linkBtn.querySelector('span');
      var origLinkText = linkTextSpan ? linkTextSpan.textContent : '';

      copyTextToClipboard(url, function() {
        linkBtn.classList.add('copied');
        if (linkIcon) linkIcon.className = 'ti ti-check';
        if (linkTextSpan) linkTextSpan.textContent = 'Copied!';
        setTimeout(function() {
          linkBtn.classList.remove('copied');
          if (linkIcon) linkIcon.className = 'ti ti-link';
          if (linkTextSpan) linkTextSpan.textContent = origLinkText;
        }, 2000);
      });
      return;
    }
  });
})();
