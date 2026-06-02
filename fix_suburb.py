import os

niches = ['gyms', 'camping', 'dog-parks', 'markets', 'pools', 'skate-parks', 'playgrounds', 'tennis-courts', 'ev-charging', 'libraries', 'restaurants', 'cafes', 'chemists', 'petrol-stations', 'parks', 'beaches', 'medical-centres', 'dentists', 'vets', 'childcare', 'supermarkets', 'hardware-stores', 'post-offices', 'banks', 'petshops', 'bakeries', 'hairdressers', 'car-washes', 'mechanics', 'bottle-shops']

descs = {
    'gyms': 'Find gyms and fitness centres near you across every state in Australia.',
    'camping': 'Find free campsites and caravan parks near you across every state in Australia.',
    'dog-parks': 'Find off leash dog parks and dog beaches near you across every state in Australia.',
    'markets': 'Find farmers markets and weekend markets near you across every state in Australia.',
    'pools': 'Find public swimming pools and aquatic centres near you across every state in Australia.',
    'skate-parks': 'Find skate parks near you across every state in Australia.',
    'playgrounds': 'Find playgrounds and play areas near you across every state in Australia.',
    'tennis-courts': 'Find public tennis courts near you across every state in Australia.',
    'ev-charging': 'Find EV charging stations near you across every state in Australia.',
    'libraries': 'Find public libraries near you across every state in Australia.',
    'restaurants': 'Find restaurants and dining near you across every state in Australia.',
    'cafes': 'Find cafes and coffee shops near you across every state in Australia.',
    'chemists': 'Find pharmacies and chemists near you across every state in Australia.',
    'petrol-stations': 'Find petrol stations and service stations near you across every state in Australia.',
    'parks': 'Find parks and reserves near you across every state in Australia.',
    'beaches': 'Find beaches and surf spots near you across every state in Australia.',
    'medical-centres': 'Find GP clinics and medical centres near you across every state in Australia.',
    'dentists': 'Find dentists and dental clinics near you across every state in Australia.',
    'vets': 'Find veterinarians and vet clinics near you across every state in Australia.',
    'childcare': 'Find childcare centres and kindergartens near you across every state in Australia.',
    'supermarkets': 'Find supermarkets and grocery stores near you across every state in Australia.',
    'hardware-stores': 'Find hardware stores and trade suppliers near you across every state in Australia.',
    'post-offices': 'Find post offices and Australia Post locations near you across every state in Australia.',
    'banks': 'Find banks and ATMs near you across every state in Australia.',
    'petshops': 'Find pet shops and pet supply stores near you across every state in Australia.',
    'bakeries': 'Find bakeries and bread shops near you across every state in Australia.',
    'hairdressers': 'Find hairdressers and hair salons near you across every state in Australia.',
    'car-washes': 'Find car washes and detailing services near you across every state in Australia.',
    'mechanics': 'Find mechanics and auto repair shops near you across every state in Australia.',
    'bottle-shops': 'Find bottle shops and liquor stores near you across every state in Australia.',
}

for niche in niches:
    filepath = f'src/pages/{niche}.astro'
    if not os.path.exists(filepath): continue
    with open(filepath, 'r') as f: content = f.read()
    content = content.replace(
        'Find gyms, fitness centres and CrossFit boxes near you across every state and suburb in Australia.',
        descs[niche]
    )
    content = content.replace(
        'Find listings near you across every state and suburb in Australia.',
        descs[niche]
    )
    with open(filepath, 'w') as f: f.write(content)
    print(f'Fixed: {niche}')

print('Done!')