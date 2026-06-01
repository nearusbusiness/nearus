import fetch from 'node-fetch';
import fs from 'fs';

const API_KEY = 'AIzaSyAqs8_xoST3b5qrXBSI6-tDmFDwfUDD1ho'; // paste your key here

const searchAreas = [
  // NSW
  { query: 'gym in Sydney NSW', state: 'NSW' },
  { query: 'gym in Newcastle NSW', state: 'NSW' },
  { query: 'gym in Wollongong NSW', state: 'NSW' },
  { query: 'gym in Central Coast NSW', state: 'NSW' },
  { query: 'gym in Parramatta NSW', state: 'NSW' },
  // VIC
  { query: 'gym in Melbourne VIC', state: 'VIC' },
  { query: 'gym in Geelong VIC', state: 'VIC' },
  { query: 'gym in Ballarat VIC', state: 'VIC' },
  { query: 'gym in Bendigo VIC', state: 'VIC' },
  // QLD
  { query: 'gym in Brisbane QLD', state: 'QLD' },
  { query: 'gym in Gold Coast QLD', state: 'QLD' },
  { query: 'gym in Sunshine Coast QLD', state: 'QLD' },
  { query: 'gym in Townsville QLD', state: 'QLD' },
  { query: 'gym in Cairns QLD', state: 'QLD' },
  // WA
  { query: 'gym in Perth WA', state: 'WA' },
  { query: 'gym in Fremantle WA', state: 'WA' },
  { query: 'gym in Joondalup WA', state: 'WA' },
  { query: 'gym in Mandurah WA', state: 'WA' },
  { query: 'gym in Bunbury WA', state: 'WA' },
  // SA
  { query: 'gym in Adelaide SA', state: 'SA' },
  { query: 'gym in Mount Gambier SA', state: 'SA' },
  { query: 'gym in Whyalla SA', state: 'SA' },
  // TAS
  { query: 'gym in Hobart TAS', state: 'TAS' },
  { query: 'gym in Launceston TAS', state: 'TAS' },
  { query: 'gym in Devonport TAS', state: 'TAS' },
  // ACT
  { query: 'gym in Canberra ACT', state: 'ACT' },
  // NT
  { query: 'gym in Darwin NT', state: 'NT' },
  { query: 'gym in Alice Springs NT', state: 'NT' },
];

async function searchPlaces(query, state) {
  const url = `https://maps.googleapis.com/maps/api/place/textsearch/json?query=${encodeURIComponent(query)}&key=${API_KEY}`;
  const res = await fetch(url);
  const data = await res.json();

  if (!data.results) return [];

  return data.results.map(place => ({
    name: place.name,
    address: place.formatted_address,
    suburb: place.formatted_address.split(',')[1]?.trim() || '',
    state: state,
    lat: place.geometry?.location?.lat,
    lng: place.geometry?.location?.lng,
    place_id: place.place_id,
    maps_url: `https://www.google.com/maps/place/?q=place_id:${place.place_id}`,
  }));
}

async function scrapeAll() {
  const allGyms = [];
  const seen = new Set();

  for (const area of searchAreas) {
    console.log(`Scraping: ${area.query}`);
    const results = await searchPlaces(area.query, area.state);

    for (const gym of results) {
      if (!seen.has(gym.place_id)) {
        seen.add(gym.place_id);
        allGyms.push(gym);
      }
    }

    // Delay to avoid rate limiting
    await new Promise(r => setTimeout(r, 500));
  }

  fs.mkdirSync('src/data', { recursive: true });
  fs.writeFileSync('src/data/gyms.json', JSON.stringify(allGyms, null, 2));
  console.log(`Done! Saved ${allGyms.length} gyms to src/data/gyms.json`);
}

scrapeAll();