
file_name = "data.csv"
formatted_file_name = "new_data.csv"

with open(file_name) as datafile:
    data_lines = datafile.readlines()

split_data_lines = [row.strip().rsplit(";") for row in data_lines]

with open(formatted_file_name, "a") as formatted_datafile:
    for row in split_data_lines:
        grams = row[0].replace(".", ",")

        date = row[2].rsplit("/")
        month = date[0]
        day = date[1]
        year = date[2]
        formatted_date = f"{day}.{month}.{year}"

        raw_time = row[3].rsplit(":")
        hours = int(raw_time[0])
        minutes = raw_time[1]
        raw_seconds = raw_time[2]
        if "odp." in raw_seconds:
            if hours != 12:
                hours += 12
            seconds = raw_seconds.replace(" odp.", "")
        else:
            seconds = raw_seconds.replace(" dop.", "")
        time = f"{hours}:{minutes}:{seconds}"

        formatted_row = f"{formatted_date} {time};{grams};\n"
        formatted_datafile.write(formatted_row)
