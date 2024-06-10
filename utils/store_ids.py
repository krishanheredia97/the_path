def store_ids(role_ids=None, channel_ids=None):
    file_path = r"C:\Users\danie\PycharmProjects\the_path\utils\test_ids.txt"

    with open(file_path, "r+") as file:
        lines = file.readlines()
        roles_line = next((line for line in lines if line.startswith("ROLES:")), "ROLES: \n")
        channels_line = next((line for line in lines if line.startswith("CHANNELS:")), "CHANNELS: \n")

        # Remove the lines we're going to update
        lines = [line for line in lines if not line.startswith("ROLES:") and not line.startswith("CHANNELS:")]

        if role_ids:
            # Update roles line with space-separated IDs
            roles_line = roles_line.strip() + " " + " ".join(map(str, role_ids)) + "\n"

        if channel_ids:
            # Update channels line with space-separated IDs
            channels_line = channels_line.strip() + " " + " ".join(map(str, channel_ids)) + "\n"

        # Rewrite the file with the updated lines
        file.seek(0)
        file.writelines(lines + [roles_line, channels_line])
        file.truncate()
