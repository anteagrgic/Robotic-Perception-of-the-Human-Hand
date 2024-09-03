import csv



with open('data_base_transformed.csv', 'r') as file:
    reader = csv.reader(file)
    header = next(reader)

    id_index = header.index('ID')

    header.remove('ID')

    modified_rows = [header]

    for row in reader:
        del row[id_index]
        modified_rows.append(row)

with open('data_base_transformed_2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(modified_rows)

