import sys

from drawer.svg.contribution_game_svg import ContributionGameSVG


def main():
    user_name = sys.argv[1]
    token = sys.argv[2]
    lizard_color = sys.argv[3] if len(sys.argv) > 3 else None

    for theme in ["light", "dark"]:
        ContributionGameSVG(
            user_name,
            token,
            theme,
            lizard_color=lizard_color
        ).run()

if __name__ == "__main__":
    main()
