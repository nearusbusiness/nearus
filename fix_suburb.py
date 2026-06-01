import os

niches = ['gyms', 'camping', 'dog-parks', 'markets', 'pools', 'skate-parks', 'playgrounds', 'tennis-courts', 'ev-charging', 'libraries', 'restaurants', 'cafes', 'chemists', 'petrol-stations', 'parks', 'beaches', 'medical-centres', 'dentists', 'vets', 'childcare', 'supermarkets', 'hardware-stores', 'post-offices', 'banks', 'petshops', 'bakeries', 'hairdressers', 'car-washes', 'mechanics', 'bottle-shops']

for niche in niches:
    filepath = f'src/pages/{niche}.astro'
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r') as f:
        content = f.read()

    # Add suburb dropdown if missing
    if 'suburb-filter' not in content:
        content = content.replace(
            '<select id="sort-filter">',
            '<select id="suburb-filter"><option value="">All Suburbs</option></select>\n    <select id="sort-filter">'
        )

    # Replace everything from first <script> to end of file
    start = content.find('<script>')
    if start != -1:
        content = content[:start].rstrip()

    # Append single clean script
    content += f"""

<script>
  let allData = [];
  let filtered = [];
  let shown = 48;

  function renderCards() {{
    const grid = document.getElementById('results-grid');
    const count = document.getElementById('results-count');
    if (!grid) return;
    const cards = filtered.slice(0, shown);
    if (count) count.textContent = 'Showing ' + Math.min(shown, filtered.length).toLocaleString() + ' of ' + filtered.length.toLocaleString() + ' listings';
    grid.innerHTML = cards.map(item => '<a href="' + item.maps_url + '" target="_blank" rel="noopener" class="result-card">' +
      '<div class="result-card-name">' + item.name + '</div>' +
      '<div class="result-card-loc">📍 ' + item.address + '</div>' +
      (item.rating ? '<div class="result-card-rating">⭐ ' + item.rating + ' (' + (item.total_ratings || 0).toLocaleString() + ' reviews)</div>' : '') +
      '<span class="result-card-state">' + item.state + '</span>' +
      '</a>').join('');
  }}

  function applyFilters() {{
    const search = (document.getElementById('search-input')?.value || '').toLowerCase();
    const state = document.getElementById('state-filter')?.value || '';
    const suburb = document.getElementById('suburb-filter')?.value || '';
    const sort = document.getElementById('sort-filter')?.value || 'rating';

    filtered = allData.filter(g => {{
      const matchSearch = !search || g.name.toLowerCase().includes(search) || g.suburb.toLowerCase().includes(search) || (g.address || '').toLowerCase().includes(search);
      const matchState = !state || g.state === state;
      const matchSuburb = !suburb || g.suburb === suburb;
      return matchSearch && matchState && matchSuburb;
    }});

    if (sort === 'rating') filtered.sort((a, b) => (b.rating || 0) - (a.rating || 0));
    if (sort === 'name') filtered.sort((a, b) => a.name.localeCompare(b.name));
    if (sort === 'reviews') filtered.sort((a, b) => (b.total_ratings || 0) - (a.total_ratings || 0));

    shown = 48;
    renderCards();
  }}

  document.getElementById('search-input')?.addEventListener('input', applyFilters);
  document.getElementById('state-filter')?.addEventListener('change', () => {{
    const state = document.getElementById('state-filter')?.value || '';
    const suburbEl = document.getElementById('suburb-filter');
    if (suburbEl) {{
      const suburbs = [...new Set(allData.filter(g => !state || g.state === state).map(g => g.suburb).filter(Boolean))].sort();
      suburbEl.innerHTML = '<option value="">All Suburbs</option>' + suburbs.map(s => '<option value="' + s + '">' + s + '</option>').join('');
    }}
    applyFilters();
  }});
  document.getElementById('suburb-filter')?.addEventListener('change', applyFilters);
  document.getElementById('sort-filter')?.addEventListener('change', applyFilters);
  document.getElementById('load-more')?.addEventListener('click', () => {{ shown += 48; renderCards(); }});

  window.addEventListener('load', async () => {{
    try {{
      const res = await fetch('/{niche}-data.json');
      allData = await res.json();
      filtered = [...allData];
      const suburbEl = document.getElementById('suburb-filter');
      if (suburbEl) {{
        const suburbs = [...new Set(allData.map(g => g.suburb).filter(Boolean))].sort();
        suburbEl.innerHTML = '<option value="">All Suburbs</option>' + suburbs.map(s => '<option value="' + s + '">' + s + '</option>').join('');
      }}
      applyFilters();
    }} catch(e) {{
      console.error('Failed to load data', e);
    }}
  }});
</script>
"""

    with open(filepath, 'w') as f:
        f.write(content)
    print(f'Fixed: {niche}')

print('All done!')