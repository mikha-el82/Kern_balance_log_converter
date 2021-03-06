import datetime


file_name = input("Name of the file to convert (excl. '.csv'): ") + ".csv"
formatted_file_name = input("Name of the formatted file (excl. '.csv'): ") + ".csv"
dish_weight_str = input("Empty Petri dish weight [g]: ")
dish_weight = float(dish_weight_str)
excel_file_name = formatted_file_name.replace(".csv", ".xlsx")
dish_weight_row = f"Hmotnost prázdné Petriho misky [g]:;{dish_weight_str.replace('.', ',')}\n"
header_row = "Datum;Hmotnost [g];Hmotnost malty [g];Uplynulý čas [hh:hh:ss];Uplynulý čas [h]; m/m0\n"

with open(file_name) as datafile:
    data_lines = datafile.readlines()

split_data_lines = [row.strip().rsplit(";") for row in data_lines]

with open(formatted_file_name, "a") as formatted_datafile:
    formatted_datafile.write(dish_weight_row)
    formatted_datafile.write(header_row)
    number_of_rows = 0
    for row in split_data_lines:
        number_of_rows += 1
        if "initial_grams" not in globals():
            initial_grams = float(row[0])-dish_weight
            print(f"Initial weight of mortar: {initial_grams}")
        grams = float(row[0])
        grams_comma = str(grams).replace(".", ",")
        grams_mortar = grams - dish_weight
        grams_mortar_comma = str(grams_mortar).replace(".", ",")
        ratio = round(grams_mortar / initial_grams, 4)
        ratio_comma = str(ratio).replace(".", ",")

        if "/" in row[2]:
            date = row[2].rsplit("/")
            month = int(date[0])
            day = int(date[1])
            year = int(date[2])
        if "." in row[2]:
            date = row[2].rsplit(".")
            month = int(date[0])
            day = int(date[1])
            year = int(date[2])

        formatted_date = f"{day}.{month}.{year}"

        raw_time = row[3].rsplit(":")
        hours = int(raw_time[0])
        minutes = int(raw_time[1])
        raw_seconds = raw_time[2]
        if "odp." in raw_seconds:
            if hours != 12:
                hours += 12
            seconds = int(raw_seconds.replace(" odp.", ""))
        else:
            if hours == 12:
                hours = 0
            seconds = int(raw_seconds.replace(" dop.", ""))
        if minutes < 10:
            minutes_str = f"0{minutes}"
        else:
            minutes_str = str(minutes)
        if seconds < 10:
            seconds_str = f"0{seconds}"
        else:
            seconds_str = str(seconds)
        formatted_time = f"{hours}:{minutes_str}:{seconds_str}"

        if "initial_datetime" not in globals():
            initial_datetime = datetime.datetime(year, month, day, hours, minutes, seconds)
            print(f"Initial datetime: {initial_datetime}")

        current_datetime = datetime.datetime(year, month, day, hours, minutes, seconds)
        elapsed_time = current_datetime - initial_datetime
        elapsed_days = elapsed_time.days
        elapsed_hours, remainder = divmod(elapsed_time.seconds, 3600)
        elapsed_minutes, elapsed_seconds = divmod(remainder, 60)
        elapsed_hours = elapsed_hours + elapsed_days * 24
        elapsed_formatted = f"{elapsed_hours}:{elapsed_minutes}:{elapsed_seconds}"
        elapsed_time_hours_only = round(elapsed_hours + elapsed_minutes / 60 + elapsed_seconds / 3600, 4)
        elapsed_time_hours_only_comma = str(elapsed_time_hours_only).replace(".", ",")

        formatted_row = f"{formatted_date} {formatted_time};{grams_comma};{grams_mortar_comma};{elapsed_formatted};" \
                        f"{elapsed_time_hours_only_comma};{ratio_comma}\n "
        formatted_datafile.write(formatted_row)

print(f"Elapsed time: {elapsed_time}")
print(f"Number of rows: {number_of_rows}")
