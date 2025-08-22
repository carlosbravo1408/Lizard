# 🦎Lizard

Spawns a lizard that devours insects that appear in your contribution graph.

<p align="center">
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/carlosbravo1408/Lizard/output/contribution_map_animation_dark.svg">
        <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/carlosbravo1408/Lizard/output/contribution_map_animation_light.svg">
        <img alt="Github contribution lizard Animation" src="github-lizard.svg" />
    </picture>
</p>

## 📖 About

**ContributionGame** is a playful project that brings life to your GitHub contribution graph by animating a lizard chasing and devouring insects that spawn on your activity squares.

The idea draws inspiration from several creative works:

- [Platane/snk](https://github.com/Platane/snk) 🐍, the famous GitHub snake animation.
- [argonautcode/animal-proc-anim](https://github.com/argonautcode/animal-proc-anim) 🦎🐍🐟, a procedural animal animation project (originally featured in [this video](https://www.youtube.com/watch?v=qlfh_rv6khY)).
- [zappo2/digital-art-with-matlab](https://github.com/zappo2/digital-art-with-matlab/blob/master/creatures/lizardFollowsMouse.m)🦎, particularly the **Lizard Follows Mouse** concept in MATLAB.

This project is meant as both a creative experiment and a fun way to personalize your GitHub profile.

## ⚙️ Usage with Cronjob

The animation is automatically generated through a GitHub Action workflow.
 A **cron job** is set to periodically regenerate the lizard animation, ensuring that it stays up-to-date with your latest contributions.

```yaml
name: generate contribution SVGs

on:
  schedule:
    - cron: "0 0 * * *"  # each 24 hours
  workflow_dispatch:
  push:
    branches:
      - main

jobs:
  generate:
    permissions:
      contents: write
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Generate lizard
        uses: carlosbravo1408/Lizard@v1
        with:
          user_name: ${{ github.repository_owner }}
          token: ${{ secrets.GITHUB_TOKEN }}
          outputs: |
            dist/contribution_map_animation_light.svg
            dist/contribution_map_animation_dark.svg

      - name: Commit and push SVG
        uses: crazy-max/ghaction-github-pages@v3.1.0
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

The generated files are placed in the `output/` branch and made available via:

- `output/contribution_map_animation_dark.svg` 🌑
- `output/contribution_map_animation_light.svg` ☀️

## 🎨 Themes

The project automatically generates **two versions of the animation**:

- One optimized for **dark mode**
- One optimized for **light mode**

GitHub’s `<picture>` element is used to seamlessly switch between them depending on the user’s preferred theme.

```html
<picture>
    <source media="(prefers-color-scheme: dark)" srcset="source/to/contribution_map_animation_dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="source/to/contribution_map_animation_light.svg">
    <img alt="Github contribution lizard Animation" src="github-lizard.svg" />
</picture>
```



## 🤝 Contributing

This project does not accept pull requests.
Reporting or fixing issues is appreciated, but changes to the API or core implementation should be discussed in an issue first and are likely not to be greenlighted.