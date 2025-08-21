from typing import List, Optional, Dict, Any

import requests

from .daily_contribution import DailyContribution
from .weekly_contributions import WeeklyContributions


class GithubFetcher:
    def __init__(self, user_name: str, token: str) -> None:
        self._user_name = user_name
        self._token = token

    def _get_contribution_graph(self) -> Optional[Dict[str, Any]]:
        url = "https://api.github.com/graphql"
        query = f"""
            query {{
              user(login: "{self._user_name}") {{
                contributionsCollection {{
                  contributionCalendar {{
                    weeks {{
                      contributionDays {{
                        date
                        weekday
                        contributionCount
                        contributionLevel
                      }}
                    }}
                  }}
                }}
              }}
            }}
        """
        headers = {
            "Authorization": f"bearer {self._token}"
        }
        r = requests.post(url, json={"query": query}, headers=headers)
        if r.status_code == 200:
            return r.json()
        return None

    def get_daily_contributions(self) -> Optional[List[DailyContribution]]:
        response = self._get_contribution_graph()
        if response is None:
            return None
        contributions = response \
            .get("data") \
            .get("user") \
            .get("contributionsCollection") \
            .get("contributionCalendar")
        weeks = [
            WeeklyContributions(week.get('contributionDays'), i)
            for i, week in enumerate(contributions.get("weeks"))
        ]
        days = []
        for week in weeks:
            days.extend(week.contribution_stats)
        return days
