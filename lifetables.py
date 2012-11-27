from os import listdir
from timeleft.models import LifeTableEntry

LIFE_TABLE_DIR = 'lifetables'

def update_lifetables():
    # Assumes no subdirectories in life table directory
    filenames = listdir(LIFE_TABLE_DIR)
    for filename in filenames:
        file = open(LIFE_TABLE_DIR + '/' + filename)

        current_country = ""
        current_gender = ""
        current_year_of_table = ""

        lines = file.readlines()

        first_line = lines[0]
        last_line = lines[-1]

        current_country = first_line.split(',')[0]

        if 'Females' in first_line:
            current_gender = 'F'
        else:
            current_gender = 'M'

        current_year_of_table = last_line.split()[0]

        print "Processing: ", current_country, current_gender, current_year_of_table

        # Read the lines starting at the end
        for line in reversed(lines):
            age = ""
            probability_of_death_before_next_bday = ""
            projected_years_left = ""

            # For each entry in the latest year
            table_row_data = line.split()
            check_year = table_row_data[0]
            if check_year == current_year_of_table:
                # Get the current age
                age = table_row_data[1]
                if '+' in age:
                    age = age[:-1] # Remove the plus sign if necessary

                # Get the probability of death before the next birthday
                probability_of_death_before_next_bday = table_row_data[2]
                # Get the projected years left
                projected_years_left = table_row_data[-1]

                # Save all the current entry data to the database
                table_entry = LifeTableEntry.objects.create(
                    country = current_country,
                    year_updated = int(current_year_of_table),
                    is_male = (current_gender == 'M'),
                    age = int(age),
                    probability_of_death_before_next_birthday = float(probability_of_death_before_next_bday),
                    remaining_years_left = float(projected_years_left)
                )

                table_entry.save()

            # If the entry is not in the lastest year
            else:
                # We have completed reading all the relevant info from this
                # file
                break

    return
