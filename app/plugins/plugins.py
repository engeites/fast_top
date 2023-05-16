from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any


class PluginInterface(ABC):
    @abstractmethod
    def analyze(self, data: list[dict[str, Any]]) -> dict[str, Any]:
        pass


class DialogsCreated(PluginInterface):
    @staticmethod
    def analyze(data: list[dict[str, Any]]):
        def prettify(data: int) -> None:
            print(f"Number of dialogs created: {data}")

        # calculate total amount of entries in data['started']
        return {
            'dialogs created':
                {
            'args': len(data['started']),
            'func': prettify,
            'desc':  "Number of dialogs created",
            'type': "basic"
                }
        }

class SuccessRechargePlugin(PluginInterface):
    @staticmethod
    def analyze(data: list[dict[str, Any]]) -> dict[str, Any]:
        def prettify(data: int) -> None:
            print(f"Total successful top-ups: {data}")

        # calculate total amount of entries in data['succeed']
        return {'Successful recharges':{
            'args': len(data['succeed']),
            'func': prettify,
            'desc': "Total successful top-ups",
            'type': "basic"}
        }


class RechargedAmountPlugin(PluginInterface):
    @staticmethod
    def analyze(data: list[dict[str, Any]]) -> dict[str, Any]:
        def prettify(data: int) -> None:
            print(f"Recharged amount: {data}")

        # calculate sum of all entries in data['succeed']['coin']
        return {'total recharged amount':
                    {'args': sum([int(entry["coin"]) for entry in data["succeed"]]),
                     'func':  prettify,
                     'desc': "Total recharged amount",
                     'type': "basic"}
                }


class FailedRechargePlugin(PluginInterface):
    @staticmethod
    def analyze(data: list[dict[str, Any]]) -> dict[str, Any]:
        def prettify(data: int) -> None:
            print(f"Recharges failed: {data}")

        # calculate total amount of entries in data['failed']
        return {'failed_recharges':
                    {'args': len(data['interrupted']),
                     'func': prettify,
                     'desc': "Number of dialogs interrupted",
                     'type': "basic"}
                }


class RechargedUsers(PluginInterface):
    @staticmethod
    def analyze(data: list[dict[str, Any]]) -> dict[str, Any]:
        def prettify(user_list: list) -> None:
            print(f"Recharged users list: ")
            for user in user_list:
                print(f"User ID {user['user']} recharged {user['recharge_amount']} coins")

        # get list of 'user' entries in data['succeed']
        users = [{'user': entry['user'], 'recharge_amount': entry['coin']} for entry in data['succeed']]
        return {'recharged users':
                    {'args': users,
                     'func': prettify,
                     'desc': "User recharge details",
                     'type': "detailed"}
                }


class AgentRecharges(PluginInterface):
    @staticmethod
    def analyze(data: list[dict[str, Any]]) -> dict[str, Any]:
        def prettify(agent_list: list) -> None:
            for agent in agent_list:
                print(f"Agent {agent['agent']} recharged {agent['coins']} coins")

        # get list of 'agent' entries in data['succeed']
        agents = [{'agent': entry['agent'], 'coin': entry['coin']} for entry in data['succeed']]

        # get list of agents and their total amount of coins
        agents = list(set([int(agent['agent']) for agent in agents]))
        new_result = [{'agent': agent, 'coins': sum([entry['coin'] for entry in data['succeed'] if int(entry['agent']) == agent])} for agent in agents]

        return {'agent recharges':
                    {'args': new_result,
                     'func': prettify,
                     'desc': "Agent recharge details",
                     'type': "detailed"}
                }


class DialogsByTime(PluginInterface):
    # Ananlyze how many dialogs were created in each hour
    @staticmethod
    def analyze(data: list[dict[str, Any]]) -> dict[str, Any]:
        def prettify(data: list) -> None:
            print("New dialogs created by time:")
            for line in data:
                print(line)

        count_by_hour = defaultdict(int)

        for entry in data['started']:
            hour = datetime.fromisoformat(entry['time']).strftime('%H')
            count_by_hour[hour] += 1

        result = [{'%02d' % int(hour): count} for hour, count in count_by_hour.items()]
        result = sorted(result, key=lambda x: next(iter(x)))

        return {'dialogs created by time': {'args': result, 'func': prettify, 'desc': "Sort dialogs by time", 'type': "detailed"}}


class RechargeTime(PluginInterface):
    @staticmethod
    def analyze(data: dict[str, Any]) -> dict[str, Any]:
        def prettify(data: dict) -> None:
            timedeltas = []
            for user, time_difference in data.items():
                print(f"{user}: recharge time = {time_difference.total_seconds()} secs")
                timedeltas.append(time_difference)

            total_seconds = sum(delta.total_seconds() for delta in timedeltas)
            average_seconds = total_seconds / len(timedeltas)
            print(f"\nAverage recharge time = {average_seconds} secs")

        started_entries = data['started']
        succeed_entries = data['succeed']

        user_times = {}  # Dictionary to store time difference for each user

        for entry in succeed_entries:
            user = str(entry['user'])  # Convert user ID to string for comparison

            if user in user_times:
                continue  # Skip if user already processed

            matching_started_entries = [started for started in started_entries if str(started['user']) == user]

            if len(matching_started_entries) == 1:
                started_time = datetime.strptime(matching_started_entries[0]['time'], "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
                succeed_time = datetime.strptime(entry['time'], "%Y-%m-%d %H:%M:%S")
                time_difference = succeed_time - started_time
                user_times[user] = time_difference

        return {'recharge time by user':
                    {'args': user_times,
                     'func': prettify,
                     'desc': "Recharge time by user",
                     'type': "detailed"
                     }
                }


class AgentAverageRechargeTime(PluginInterface):
    @staticmethod
    def analyze(data: dict[str, Any]) -> dict[str, Any]:
        def prettify(agents: dict) -> None:
            average_seconds = {}
            count = {}
            for key, value in agents.items():
                time_difference = value['time_difference']
                seconds = time_difference.total_seconds()
                key_id = value['id:']
                if key_id not in average_seconds:
                    average_seconds[key_id] = seconds
                    count[key_id] = 1
                else:
                    average_seconds[key_id] += seconds
                    count[key_id] += 1

            print("\nAverage recharge time by agent:")
            # Calculate the average seconds for each key
            for key, value in average_seconds.items():
                average = value / count[key]
                print(f"{key}: {average} seconds")

        started_entries = data['started']
        succeed_entries = data['succeed']

        agent_times = {}  # Dictionary to store time difference for each user

        for entry in succeed_entries:
            user = str(entry['user'])  # Convert user ID to string for comparison

            matching_started_entries = [started for started in started_entries if str(started['user']) == user]

            if len(matching_started_entries) == 1:
                started_time = datetime.strptime(matching_started_entries[0]['time'], "%Y-%m-%dT%H:%M:%S%z").replace(
                    tzinfo=None)
                succeed_time = datetime.strptime(entry['time'], "%Y-%m-%d %H:%M:%S")
                time_difference = succeed_time - started_time
                agent_times[entry['user']] = {'id:':  entry['agent'], 'user': entry['user'], 'time_difference': time_difference}

        return {'recharge time by agent': {'args': agent_times,
                                           'func': prettify,
                                           'desc': "Average recharge time by agent",
                                           'type': "detailed"
                                           }
                }


class ChannelEffectiveness(PluginInterface):
    @staticmethod
    def analyze(data: dict[str, Any]) -> dict[str, Any]:
        def prettify(effectiveness: float) -> None:
            print(f"Channel effectiveness: {effectiveness:.1%}")

        started_count = len(data['started'])
        succeed_count = len(data['succeed'])

        effectiveness_ratio = succeed_count / started_count if started_count > 0 else 0
        return {'channel effectiveness': {'args': effectiveness_ratio,
                                          'func': prettify,
                                          'desc': "Channel effectiveness",
                                          'type': "basic"
                                          }
                }