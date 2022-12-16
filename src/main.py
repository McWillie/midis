import random

from users import Administrator, Volunteer


def main():
    # Create an administrator
    mr_admin = Administrator(True, 'Bossman')
    # Create a volunteer that exercises the validation rules (wrong names accepted, but a warning is printed as per requirements)
    mr_volunteer = Volunteer(False, "Tree", "James 3d", -42, "Grove street 2", "j.tree", "+31 68-22-555")

    # Add a photo for Mr. Volunteer
    mr_volunteer.add_user_photo("my_photo.jpg")
    # Save photo in user photos folder
    mr_volunteer.write_user_photo("user_photos")

    # Create and print email recipient line
    print("Mr. Volunteers email line: ", mr_volunteer.create_recipient())
    # Print birth year and phone number to show defaults and cleanup
    print("Mr. Volunteer's defaulted birth year: ", mr_volunteer.birth_year)
    print("Mr. Volunteer's clean phone number: ", mr_volunteer.phone, '\n')

    # Add garbage collection data for Mr. Volunteer
    day = 1
    for i in range(10):
        mr_volunteer.add_collection_data(
            random.choice(('glass', 'paper', 'plastic')),
            random.randrange(1, 30),
            random.random(),
            f'2022-12-{day}')
        day += 1
    # Print collection data for Mr. Volunteer
    mr_volunteer.print_collection_data()
    # Print collected glass garbage sum total for the first 5 days (rerun script if 0)
    print('Mr. Volunteer collected', mr_volunteer.garbage_sum('glass', 'weight', '2022-12-1', '2022-12-5'), 'kgs', 'of glass garbage.', '\n')
    # Print volunteer garbage collection summary
    mr_volunteer.print_sum_stats()


if __name__ == "__main__":
    main()
