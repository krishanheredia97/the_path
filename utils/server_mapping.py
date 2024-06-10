from backend.data_manager import save_server_mapping_data, load_server_mapping


async def save_server_mapping(guild, role_ids, categories):
    # Create the structure to store the mapping
    server_structure = {
        "roles": [],
        "categories": [],
        "variables": {}
    }

    # Order roles by hierarchy
    role_hierarchy = ["Peasant", "Esquire", "Knight", "Noble"]
    for role in role_hierarchy:
        if role in role_ids:
            server_structure["roles"].append({"name": role, "id": str(role_ids[role])})

    # Add categories and channels
    for category in categories:
        category_info = {
            "name": category["name"],
            "id": str(category["id"]),
            "channels": [{"name": channel["name"], "id": str(channel["id"])} for channel in category["channels"]]
        }
        server_structure["categories"].append(category_info)

        # Check for specific channels to add to variables
        if category["name"] == "QUEST CREATION":
            for channel in category["channels"]:
                if channel["name"] == "✅│quest-review":
                    server_structure["variables"]["REVIEW_QUEST_CHANNEL_ID"] = str(channel["id"])
                elif channel["name"] == "📝│quest-proposals":
                    server_structure["variables"]["CREATE_QUEST_CHANNEL_ID"] = str(channel["id"])
        elif category["name"] == "HABIT TRACKING":
            for channel in category["channels"]:
                if channel["name"] == "🟡│vices":
                    server_structure["variables"]["VICES_ID"] = str(channel["id"])
        elif category["name"] == "REWARDS":
            for channel in category["channels"]:
                if channel["name"] == "🟡│rewards":
                    server_structure["variables"]["REWARDS_ID"] = str(channel["id"])
        elif category["name"] == "INFORMATION":
            for channel in category["channels"]:
                if channel["name"] == "🔧│settings":
                    server_structure["variables"]["SETTINGS_ID"] = str(channel["id"])

    # Load the existing server data from Firebase
    existing_server_data = load_server_mapping(guild.id)

    # Merge the new server structure with the existing data
    merged_data = {**existing_server_data, **server_structure}

    # Save the merged data to Firebase
    save_server_mapping_data(guild.id, merged_data)

