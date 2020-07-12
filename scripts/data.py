import requests
from yaml import safe_load
import json


def get():
    with open("config.yml", "r") as file:
        config = safe_load(file)
    page = 0
    users = {}
    q = 0
    i = 0
    while i < int(config["data"]["range"] / 100):
        r = requests.get(
            f"https://mee6.xyz/api/plugins/levels/leaderboard/{config['server_id']}?page={str(page)}"
        ).json()
        if "status_code" in r.keys():
            if r["status_code"] == 404:
                exit("guild not found")
        if not r["players"] == []:
            for user in r["players"]:
                if q < config["data"]["range"] or q == config["data"]["range"]:
                    users[str(q)] = user
                q += 1
        else:
            break
        i += 1
        page += 1
    return users


def generate_gwaff(new_users, time):
    with open("gwaff.json") as json_file:
        gwaff = json.load(json_file)
        json_file.close()

    # update all info
    for user in new_users:
        if new_users[user]["id"] not in gwaff:
            gwaff[new_users[user]["id"]] = {
                "name": f"{new_users[user]['username']}#{new_users[user]['discriminator']}",
                "message_count": {str(time): new_users[user]["message_count"]},
                "total_xp": {str(time): new_users[user]["xp"], },
                "detailed_xp": {str(time): new_users[user]["detailed_xp"]},
                "level": {str(time): new_users[user]["level"]},
            }
        else:
            gwaff[new_users[user]["id"]][
                "name"
            ] = f"{new_users[user]['username']}#{new_users[user]['discriminator']}"
            gwaff[new_users[user]["id"]]["message_count"][str(time)] = new_users[user][
                "message_count"
            ]
            gwaff[new_users[user]["id"]]["total_xp"][str(time)] = new_users[user]["xp"]
            gwaff[new_users[user]["id"]]["detailed_xp"][str(time)] = new_users[user][
                "detailed_xp"
            ]
            gwaff[new_users[user]["id"]]["level"][str(time)] = new_users[user]["level"]

    # sort users by their total xp
    listoftuples = []
    for user in gwaff:
        listoftuples.append((gwaff[user]["total_xp"][list(gwaff[user]["total_xp"])[-1]], gwaff[user], user))
    gwaff = {}
    listoftuples.sort(key=lambda x: x[0], reverse=True)
    for user in listoftuples:
        gwaff[user[2]] = user[1]
    return gwaff
