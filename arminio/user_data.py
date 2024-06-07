import datetime
from discord.utils import get
from backend import data_manager


class User:
    def __init__(self, user_id, username, gender='m'):
        self.data = {
            "User_Main": {
                "user_id": user_id,
                "username": username,
                "gender": gender,
            },
            "User_Habits": {
                "vices": [],
                "global_relapse_count": 0,
                "global_quit_count": 0,
            },
            "User_Progress": {
                "Main_Progress": {
                    "roles": ["Peasant"],  # Default role will be added after initialization
                    "user_level": 1,
                    "User_Points": {
                        "global_user_xp": 0,
                        "user_gp": {
                            "current_gp": 0,
                            "spent_gp": 0,
                        },
                        "user_honor": {
                            "current_honor": 0,
                            "spent_honor": 0,
                        },
                        "user_hp": {
                            "current_hp": 10,
                            "spent_hp": 0,
                        }
                    },
                },
                "User_Skills": [
                    {
                        "name": "hitpoints",
                        "current_xp": 0
                    }
                ],
            },
            "User_Rewards": {
                "user_rewards": [],
            },
        }
        self.load_user_data()
        if "roles" not in self.data["User_Progress"]["Main_Progress"] or not self.data["User_Progress"]["Main_Progress"]["roles"]:
            self.data["User_Progress"]["Main_Progress"]["roles"] = ["Peasant"]  # Set default role if none exists
        self.save_user_data()

    def load_user_data(self):
        stored_data = data_manager.load_data(self.data["User_Main"]["user_id"])
        if stored_data:
            self.data.update(stored_data)
        # Ensure gender and roles are included even if not present in stored data
        if "gender" not in self.data["User_Main"]:
            self.data["User_Main"]["gender"] = 'm'
        if "roles" not in self.data["User_Progress"]["Main_Progress"]:
            self.data["User_Progress"]["Main_Progress"]["roles"] = ["Peasant"]

    def save_user_data(self):
        data_manager.save_data(self.data)

    def add_vice(self, vice_name):
        vice_name = vice_name.capitalize()
        if any(vice["name"] == vice_name for vice in self.data["User_Habits"]["vices"]):
            return False, f"'{vice_name}' already exists."
        new_vice = {
            "name": vice_name,
            "status": "Active",
            "log": [{"action": "created", "timestamp": self.current_time()}],
            "relapse_count": 0,
            "quit_count": 1,
            "last_update": self.current_time()
        }
        self.data["User_Habits"]["vices"].append(new_vice)
        self.data["User_Habits"]["global_quit_count"] += 1
        self.save_user_data()
        return True, f"'{vice_name}' has been added to your vices!"

    def relapse_vice(self, vice_name):
        self.calculate_rewards()
        for vice in self.data["User_Habits"]["vices"]:
            if vice["name"] == vice_name and vice["status"] == "Active":
                vice["status"] = "Inactive"
                vice["log"].append({"action": "relapsed", "timestamp": self.current_time()})
                vice["relapse_count"] += 1
                self.data["User_Habits"]["global_relapse_count"] += 1
                self.save_user_data()
                return True, f"You have relapsed on '{vice_name}'."
        return False, f"'{vice_name}' is not an active vice."

    def quit_vice(self, vice_name):
        self.calculate_rewards()
        for vice in self.data["User_Habits"]["vices"]:
            if vice["name"] == vice_name and vice["status"] == "Inactive":
                vice["status"] = "Active"
                vice["log"].append({"action": "quit", "timestamp": self.current_time()})
                vice["quit_count"] += 1
                vice["last_update"] = self.current_time()
                self.data["User_Habits"]["global_quit_count"] += 1
                self.save_user_data()
                return True, f"You have quit '{vice_name}'."
        return False, f"'{vice_name}' is not an inactive vice."

    def get_active_vices(self):
        return [vice["name"] for vice in self.data["User_Habits"]["vices"] if vice["status"] == "Active"]

    def get_inactive_vices(self):
        return [vice["name"] for vice in self.data["User_Habits"]["vices"] if vice["status"] == "Inactive"]

    def add_reward(self, reward_name, reward_cost):
        reward_name = reward_name.capitalize()
        if any(reward["name"] == reward_name for reward in self.data["User_Rewards"]["user_rewards"]):
            return False, f"'{reward_name}' already exists."
        new_reward = {
            "name": reward_name,
            "redeemed": False,
            "cost": reward_cost,
            "log": [{"action": "created", "timestamp": self.current_time()}]
        }
        self.data["User_Rewards"]["user_rewards"].append(new_reward)
        self.save_user_data()
        return True, f"'{reward_name}' has been added to your rewards!"

    def get_unredeemed_rewards(self):
        return [reward for reward in self.data["User_Rewards"]["user_rewards"] if not reward["redeemed"]]

    def redeem_reward(self, reward_name):
        for reward in self.data["User_Rewards"]["user_rewards"]:
            if reward["name"] == reward_name and not reward["redeemed"]:
                if self.data["User_Progress"]["Main_Progress"]["User_Points"]["user_gp"]["current_gp"] >= reward["cost"]:
                    self.data["User_Progress"]["Main_Progress"]["User_Points"]["user_gp"]["current_gp"] -= reward["cost"]
                    reward["redeemed"] = True
                    reward["log"].append({"action": "redeemed", "timestamp": self.current_time()})
                    self.save_user_data()
                    return True, f"'{reward_name}' has been redeemed!"
                else:
                    return False, "You do not have enough GP to redeem this reward."
        return False, f"'{reward_name}' is not available for redemption."

    def calculate_rewards(self):
        current_time = datetime.datetime.utcnow()
        for vice in self.data["User_Habits"]["vices"]:
            if vice["status"] == "Active":
                last_update_time = datetime.datetime.fromisoformat(vice["last_update"])
                elapsed_seconds = (current_time - last_update_time).total_seconds()
                self.data["User_Progress"]["Main_Progress"]["User_Points"]["global_user_xp"] += int(elapsed_seconds // 60)  # Add 1 XP per minute
                self.data["User_Progress"]["Main_Progress"]["User_Points"]["user_gp"]["current_gp"] += int(elapsed_seconds // 7200)  # Add 1 GP every 2 hours
                self.data["User_Progress"]["Main_Progress"]["User_Points"]["user_honor"]["current_honor"] += int(elapsed_seconds // 86400)  # Add 1 Honor every 24 hours
                self.level_up()  # Check for level up
                vice["last_update"] = current_time.isoformat()
        self.save_user_data()

    def level_up(self):
        while True:
            xp_required = 3000 * (1.4 ** (self.data["User_Progress"]["Main_Progress"]["user_level"] - 1))
            if self.data["User_Progress"]["Main_Progress"]["User_Points"]["global_user_xp"] >= xp_required:
                self.data["User_Progress"]["Main_Progress"]["user_level"] += 1
            else:
                break

    async def update_role(self, member, guild):
        role_ids = {
            "Peasant": 1242277817065144320,
            "Squire": 1242278493111324773,
            "Knight": 1242278728134823937,
            "Noble": 1242278829691502693,
            "Lord": 1242278971148599296,
            "Lady": 1242279797598453842,
            "Baron": 1242279077151510558,
            "Baroness": 1242279864707321876,
            "Duke": 1242279147229937674,
            "Duchess": 1242279930646237245,
            "Prince": 1242279703205646438,
            "Princess": 1242279738421022941,
            "King": 1242280031045160971,
            "Queen": 1242280070135939153,
            "Emperor": 1242280263602671646,
            "Empress": 1242280297568014437
        }

        level = self.data["User_Progress"]["Main_Progress"]["user_level"]
        role_names = {
            "Peasant": (1, 5),
            "Squire": (6, 10),
            "Knight": (11, 20),
            "Noble": (21, 30),
            "Lord": (31, 40),
            "Lady": (31, 40),
            "Baron": (41, 50),
            "Baroness": (41, 50),
            "Duke": (51, 60),
            "Duchess": (51, 60),
            "Prince": (61, 70),
            "Princess": (61, 70),
            "King": (71, 80),
            "Queen": (71, 80),
            "Emperor": (81, 100),
            "Empress": (81, 100)
        }

        # Remove all defined roles
        for role_name in role_names.keys():
            role = get(guild.roles, id=role_ids[role_name])
            if role in member.roles:
                await member.remove_roles(role)

        # Add the appropriate role based on the level and gender
        for role_name, (min_level, max_level) in role_names.items():
            if min_level <= level <= max_level:
                if "Lady" in role_name or "Baroness" in role_name or "Duchess" in role_name or "Princess" in role_name or "Queen" in role_name or "Empress" in role_name:
                    if self.data["User_Main"]["gender"] in ['f', 'o']:
                        new_role = get(guild.roles, id=role_ids[role_name])
                        await member.add_roles(new_role)
                        self.data["User_Progress"]["Main_Progress"]["roles"] = [role_name]
                        self.save_user_data()
                        break
                else:
                    new_role = get(guild.roles, id=role_ids[role_name])
                    await member.add_roles(new_role)
                    self.data["User_Progress"]["Main_Progress"]["roles"] = [role_name]
                    self.save_user_data()
                    break

    def current_time(self):
        return datetime.datetime.utcnow().isoformat()
