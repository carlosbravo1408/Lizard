from typing import List, Dict, Any

from .daily_contribution import DailyContribution


class WeeklyContributions:
    def __init__(
            self,
            contribution_stats: List[Dict[str, Any]],
            week_number: int
    ) -> None:
        self.contribution_stats = []
        self._week_number = week_number
        for day in contribution_stats:
            daily_contrib = DailyContribution(
                _date=day["date"],
                contributions=day["contributionCount"],
                week_number=week_number,
                day_number=day['weekday'],
                quartile=day["contributionLevel"],
            )
            self.contribution_stats.append(daily_contrib)
