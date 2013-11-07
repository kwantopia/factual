from factual import Factual
import pprint
import csv

pp = pprint.PrettyPrinter(indent=2)

factual_ids = []
with open('factual_to_naics2012.tsv', 'r') as csvfile:
  factual_id_reader = csv.DictReader(csvfile, delimiter='\t')
  for row in factual_id_reader:
    factual_ids.append({'factual_id': int(row['factual_id']), 'factual_name': row['factual_description']})

print factual_ids

factual_service = Factual('key', 'secret')

q = factual_service.table('places')

output_file = open('factual_counts.csv', 'w')

writer = csv.writer(output_file)

for fact_key in factual_ids:
  filter_query = q.filters({"$and": [{"category_ids": {'$includes': fact_key['factual_id']}}, 
                                      {"region": "ma"},
                                      {"country": "us"}, 
                                      {"chain_id":{"$blank": True}}
                                     ]}).include_count(True)

  writer.writerow([fact_key['factual_id'], fact_key['factual_name'], filter_query.total_row_count()])
  #print filter_query.total_row_count() 


#next = filter_query.offset(20)

#pp.pprint(next.data())

output_file.close()
