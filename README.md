<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a id="readme-top"></a>

<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<h3 align="center">Blaze Black/Volt White Wiki</h3>

  <p align="center">
    BBVW Wiki Generator is an automated documentation generator designed specifically for the Blaze Black and Volt White ROM hacks of Pokémon Black and White. This project processes raw game data—such as Pokémon stats, movesets, wild encounters, trainer rosters, item changes, and more—and transforms it into a clean, searchable MkDocs-powered wiki.
    <br />
    <br />
    The tool helps ROM hack developers and players alike by providing a browsable reference of in-game changes in a structured, modern web format. It combines custom Python scripts and Markdown generation to output a professional-grade wiki that can be deployed or shared with the community.
    <br />
    <br />
    <a href="https://zhenga8533.github.io/bbvw-wiki">View Demo</a>
    &middot;
    <a href="https://github.com/zhenga8533/bbvw-wiki/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/zhenga8533/bbvw-wiki/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

🧠 About This Project
BBVW Wiki Generator is a custom-built Python utility designed to automate the generation of a full documentation site for the ROM hacks Blaze Black and Volt White—popular reimaginings of Pokémon Black and White created by Drayano.

These ROM hacks introduce hundreds of game changes including:

1. Modified base stats, abilities, and movesets for all 649 Pokémon

2. New wild encounter tables across all regions

3. Reworked trainer rosters, including Gym Leaders, Rivals, and Team Plasma

4. Changes to item availability and trade evolution mechanics

5. New move learnsets and compatibility adjustments

6. Optional Action Replay codes

📦 What This Tool Does
The BBVW Wiki Generator reads and parses structured raw data files (provided as .txt files in the src/files/ directory), processes them via custom Python scripts (in the src/ directory), and generates organized, readable Markdown documentation into the docs/ directory. The final site is rendered using MkDocs, producing a clean, static site that can be hosted anywhere or viewed locally.

📚 What’s Included in the Wiki

1. Pokémon Database: Each Pokémon has a dedicated page outlining its revised stats, learnsets, evolution info, and ability changes.

2. Trainer Rosters: Pages for important NPCs and major battles show updated lineups, levels, and strategies.

3. Wild Encounters: Area-by-area breakdowns of encounter tables in caves, routes, cities, and special locations.

4. Item & Trade Info: Highlights modified held items, new trade options, and balance tweaks.

5. Code Reference: Includes documented Action Replay codes tailored for Blaze Black and Volt White.

🎯 Why This Exists
ROM hacks like BB/VW are massive in scope, and documenting every game mechanic manually is a monumental task. This project removes that overhead by automating the entire documentation pipeline. It’s especially useful for:

1. Players who want to explore and understand game mechanics in detail

2. Content creators and streamers seeking accurate reference material

3. Developers creating or modifying similar hacks

4. QA testers verifying balance and encounter changes

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![Next][Next.js]][Next-url]
- [![React][React.js]][React-url]
- [![Vue][Vue.js]][Vue-url]
- [![Angular][Angular.io]][Angular-url]
- [![Svelte][Svelte.dev]][Svelte-url]
- [![Laravel][Laravel.com]][Laravel-url]
- [![Bootstrap][Bootstrap.com]][Bootstrap-url]
- [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

- npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/zhenga8533/bbvw-wiki.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = "ENTER YOUR API";
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin zhenga8533/bbvw-wiki
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
  - [ ] Nested Feature

See the [open issues](https://github.com/zhenga8533/bbvw-wiki/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/zhenga8533/bbvw-wiki/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=zhenga8533/bbvw-wiki" alt="contrib.rocks image" />
</a>

<!-- LICENSE -->

## License

Distributed under the MIT. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - zhenga8533@gmail.com

Project Link: [https://github.com/zhenga8533/bbvw-wiki](https://github.com/zhenga8533/bbvw-wiki)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- []()
- []()
- []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/zhenga8533/bbvw-wiki.svg?style=for-the-badge
[contributors-url]: https://github.com/zhenga8533/bbvw-wiki/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/zhenga8533/bbvw-wiki.svg?style=for-the-badge
[forks-url]: https://github.com/zhenga8533/bbvw-wiki/network/members
[stars-shield]: https://img.shields.io/github/stars/zhenga8533/bbvw-wiki.svg?style=for-the-badge
[stars-url]: https://github.com/zhenga8533/bbvw-wiki/stargazers
[issues-shield]: https://img.shields.io/github/issues/zhenga8533/bbvw-wiki.svg?style=for-the-badge
[issues-url]: https://github.com/zhenga8533/bbvw-wiki/issues
[license-shield]: https://img.shields.io/github/license/zhenga8533/bbvw-wiki.svg?style=for-the-badge
[license-url]: https://github.com/zhenga8533/bbvw-wiki/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/zhenga8533
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
