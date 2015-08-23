set regions 'NA'
set game_types 'RANKED_SOLO'
#'NORMAL_5X5'
for type in $game_types
    for region in $regions
        ./manage.py load_matches 5.14/$type/$region.json 10000
    end
end
