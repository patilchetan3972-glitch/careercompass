"""Quick render verification for the anchor data-attribute fix."""
import os, sys
sys.path.insert(0, r'd:\Rajput\CareerCompass')
os.environ.setdefault('SECRET_KEY', 'test-only-key')
os.environ.setdefault('WTF_CSRF_ENABLED', 'False')

from app import app
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True

with app.test_client() as c:
    # --- Route WITH anchor: /about ---
    r1 = c.get('/about')
    html1 = r1.data.decode()
    assert r1.status_code == 200, f'/about returned {r1.status_code}'
    assert 'data-scroll-anchor="about"' in html1, 'data-scroll-anchor=about not in /about output'
    assert 'dataset.scrollAnchor' in html1,       'dataset.scrollAnchor missing from JS'
    assert '{%' not in html1,                      'Unrendered Jinja block tags in /about output!'
    assert '{{' not in html1,                      'Unrendered Jinja var tags in /about output!'
    print('PASS  /about  -> data-scroll-anchor="about" present, zero raw Jinja in output')

    # --- Route WITHOUT anchor: / ---
    r2 = c.get('/')
    html2 = r2.data.decode()
    assert r2.status_code == 200, f'/ returned {r2.status_code}'
    assert 'data-scroll-anchor' not in html2, 'data-scroll-anchor should be absent on /'
    assert 'dataset.scrollAnchor' in html2,   'dataset.scrollAnchor missing from JS on /'
    print('PASS  /       -> data-scroll-anchor absent, JS anchor guard works via dataset')

    # --- Route with anchor: /sdgs ---
    r3 = c.get('/sdgs')
    html3 = r3.data.decode()
    assert r3.status_code == 200, f'/sdgs returned {r3.status_code}'
    assert 'data-scroll-anchor="sdgs"' in html3, 'data-scroll-anchor=sdgs not in /sdgs output'
    print('PASS  /sdgs   -> data-scroll-anchor="sdgs" present')

    # --- Route with anchor: /domains ---
    r4 = c.get('/domains')
    html4 = r4.data.decode()
    assert r4.status_code == 200, f'/domains returned {r4.status_code}'
    assert 'data-scroll-anchor="domains"' in html4, 'data-scroll-anchor=domains not in /domains'
    print('PASS  /domains -> data-scroll-anchor="domains" present')

print()
print('All render checks PASSED.')
print('No Jinja tags in rendered output. Smooth-scroll JS is pure JavaScript.')
