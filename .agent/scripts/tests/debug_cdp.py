import sys
sys.path.append(r"G:\マイドライブ\Genesis_OS\.agent\scripts")
from cdp_browser import CDPBrowser

b = CDPBrowser(port=9224)
b.connect()
js = """
(function() {
    let elements = document.querySelectorAll('textarea, [contenteditable="true"]');
    let results = [];
    elements.forEach(el => {
        results.push({
            tag: el.tagName,
            id: el.id,
            className: el.className,
            placeholder: el.getAttribute('placeholder'),
            ariaLabel: el.getAttribute('aria-label'),
            value: el.value || ''
        });
    });
    return results;
})();
"""
res = b.evaluate(js)
print("Found inputs:", res)
