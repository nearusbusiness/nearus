import os

niches = ['optometrists', 'physiotherapy', 'fast-food', 'pizza', 'chinese-restaurants', 'indian-restaurants', 'sushi', 'hotels', 'real-estate', 'gyms-24hr']

titles = {
    'optometrists': 'Optometrists Near Me',
    'physiotherapy': 'Physiotherapy Near Me',
    'fast-food': 'Fast Food Near Me',
    'pizza': 'Pizza Near Me',
    'chinese-restaurants': 'Chinese Restaurants Near Me',
    'indian-restaurants': 'Indian Restaurants Near Me',
    'sushi': 'Sushi Near Me',
    'hotels': 'Hotels Near Me',
    'real-estate': 'Real Estate Agents Near Me',
    'gyms-24hr': '24 Hour Gyms Near Me',
}

descs = {
    'optometrists': 'Find optometrists and eye clinics near you across every state in Australia.',
    'physiotherapy': 'Find physiotherapists and physio clinics near you across every state in Australia.',
    'fast-food': 'Find fast food and takeaway near you across every state in Australia.',
    'pizza': 'Find pizza restaurants and delivery near you across every state in Australia.',
    'chinese-restaurants': 'Find chinese restaurants and yum cha near you across every state in Australia.',
    'indian-restaurants': 'Find indian restaurants near you across every state in Australia.',
    'sushi': 'Find sushi and japanese restaurants near you across every state in Australia.',
    'hotels': 'Find hotels and accommodation near you across every state in Australia.',
    'real-estate': 'Find real estate agents near you across every state in Australia.',
    'gyms-24hr': 'Find 24 hour gyms near you across every state in Australia.',
}

for niche in niches:
    nichevar = niche.replace('-', '')
    for filepath in [f'src/pages/{niche}.astro', f'src/pages/{niche}/[state].astro', f'src/pages/{niche}/[state]/[suburb].astro']:
        if not os.path.exists(filepath): continue
        with open(filepath, 'r') as f: content = f.read()

        content = content.replace(f"import gyms from '../data/{niche}.json'", f"import {nichevar} from '../data/{niche}.json'")
        content = content.replace(f"import gyms from '../../data/{niche}.json'", f"import {nichevar} from '../../data/{niche}.json'")
        content = content.replace(f"import gyms from '../../../data/{niche}.json'", f"import {nichevar} from '../../../data/{niche}.json'")
        content = content.replace('gymsData', f'{nichevar}Data')
        content = content.replace('const gyms ', f'const {nichevar} ')
        content = content.replace('gyms.length', f'{nichevar}.length')
        content = content.replace('gyms.slice', f'{nichevar}.slice')
        content = content.replace('gyms.map', f'{nichevar}.map')
        content = content.replace('{ gyms,', f'{{ {nichevar},')
        content = content.replace('gyms: grouped', f'{nichevar}: grouped')
        content = content.replace('for (const gym of gymsData)', f'for (const item of {nichevar}Data)')
        content = content.replace('const { gyms,', f'const {{ {nichevar},')
        content = content.replace('{gym.maps_url}', '{item.maps_url}')
        content = content.replace('{gym.name}', '{item.name}')
        content = content.replace('{gym.address}', '{item.address}')
        content = content.replace('{gym.rating}', '{item.rating}')
        content = content.replace('{gym.total_ratings', '{item.total_ratings')
        content = content.replace('{gym.state}', '{item.state}')
        content = content.replace('gym.name.toLowerCase()', 'item.name.toLowerCase()')
        content = content.replace('gym.suburb.toLowerCase()', 'item.suburb.toLowerCase()')
        content = content.replace('gym.rating', 'item.rating')
        content = content.replace('gym.total_ratings', 'item.total_ratings')
        content = content.replace('gym.state', 'item.state')
        content = content.replace('.slice(0, 48).map(gym =>', '.slice(0, 48).map(item =>')
        content = content.replace('.map((gym: any) =>', '.map((item: any) =>')
        content = content.replace('Gyms Near Me', titles[niche])
        content = content.replace('gyms and fitness centres', descs[niche])
        content = content.replace('Find gyms, fitness centres and CrossFit boxes near you across every state and suburb in Australia.', descs[niche])
        content = content.replace('Find listings near you across every state and suburb in Australia.', descs[niche])
        content = content.replace('/gyms', f'/{niche}')
        content = content.replace("fetch('/gyms-data.json')", f"fetch('/{niche}-data.json')")

        # Fix script block
        start = content.find('<script>')
        if start != -1:
            before = content[:start].rstrip()
            new_script = f"""
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
            content = before + new_script

        with open(filepath, 'w') as f: f.write(content)
    print(f'Fixed: {niche}')

print('All done!')