set regions 'NA' 'BR' 'EUNE' 'EUW' 'KR' 'LAN' 'LAS' 'OCE' 'RU' 'TR'
set game_types 'NORMAL_5X5'
for type in $game_types
    for region in $regions
        eval "./manage.py load_matches 5.14/$type/$region.json 10000"
    end
end

eval "./manage.py generate_model lasso_overnight.pkl"
