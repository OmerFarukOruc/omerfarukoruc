<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark) and (min-width: 1280px)" srcset="assets/capture-dark.svg">
  <source media="(prefers-color-scheme: light) and (min-width: 1280px)" srcset="assets/capture-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/capture-dark-narrow.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/capture-light-narrow.svg">
  <img src="assets/capture-light.svg" alt="A logic analyzer view of a UART line at 115200 baud, 8N1. Its 4 frames decode to the letters o, m, e, r.">
</picture>
</p>

I'm Omer Faruk Oruc, an embedded software engineer in İzmir, Türkiye <img src="assets/flag-tr.svg" alt="Turkish flag" height="14">.

Code that compiles proves nothing to me until I watch it run on a board. That habit comes from firmware. Now coding agents write most of my code under rules I wrote.

- [linctl](https://github.com/KyaniteHQ/linctl) is a Linear CLI you can give to an agent. The agent reads widely and writes to one team, and linctl checks every write against the live credential. There is no bypass flag.
- [nixos-config](https://github.com/OmerFarukOruc/nixos-config) is my desktop, two laptops and a server in one flake. Its `agents/` folder holds the rules, skills and hooks my agents work under. I wrote it for my own machines, so read it and copy the parts you need.
- [threadsift](https://github.com/KyaniteHQ/threadsift) is a reading library for the links I save and never get back to. An agent keeps the useful parts.
- [esp32-ntag424-terminal](https://github.com/OmerFarukOruc/esp32-ntag424-terminal) is ESP32-S3 firmware that writes NTAG424 DNA tags with a PN532 and onboards over BLE.

### Tech stack

**Embedded and systems**<br>
<img src="https://img.shields.io/badge/C-3d444d?style=flat-square&logo=c&logoColor=79c0ff" alt="C" height="22">
<img src="https://img.shields.io/badge/C%2B%2B-3d444d?style=flat-square&logo=cplusplus&logoColor=79c0ff" alt="C++" height="22">
<img src="https://img.shields.io/badge/STM32-3d444d?style=flat-square&logo=stmicroelectronics&logoColor=79c0ff" alt="STM32" height="22">
<img src="https://img.shields.io/badge/ESP32-3d444d?style=flat-square&logo=espressif&logoColor=79c0ff" alt="ESP32" height="22">
<img src="https://img.shields.io/badge/nRF_Connect-3d444d?style=flat-square&logo=nordicsemiconductor&logoColor=79c0ff" alt="nRF Connect" height="22">
<img src="https://img.shields.io/badge/Arm_Cortex--M-3d444d?style=flat-square&logo=arm&logoColor=79c0ff" alt="Arm Cortex-M" height="22">
<img src="https://img.shields.io/badge/Zephyr_RTOS-3d444d?style=flat-square" alt="Zephyr RTOS" height="22">
<img src="https://img.shields.io/badge/FreeRTOS-3d444d?style=flat-square" alt="FreeRTOS" height="22">
<img src="https://img.shields.io/badge/Embedded_Linux-3d444d?style=flat-square&logo=linux&logoColor=79c0ff" alt="Embedded Linux" height="22">
<img src="https://img.shields.io/badge/Raspberry_Pi-3d444d?style=flat-square&logo=raspberrypi&logoColor=79c0ff" alt="Raspberry Pi" height="22">
<img src="https://img.shields.io/badge/CMake-3d444d?style=flat-square&logo=cmake&logoColor=79c0ff" alt="CMake" height="22">
<img src="https://img.shields.io/badge/PlatformIO-3d444d?style=flat-square&logo=platformio&logoColor=79c0ff" alt="PlatformIO" height="22">
<img src="https://img.shields.io/badge/MQTT-3d444d?style=flat-square&logo=mqtt&logoColor=79c0ff" alt="MQTT" height="22">
<img src="https://img.shields.io/badge/Bluetooth_LE-3d444d?style=flat-square&logo=bluetooth&logoColor=79c0ff" alt="Bluetooth LE" height="22">
<img src="https://img.shields.io/badge/LoRaWAN-3d444d?style=flat-square" alt="LoRaWAN" height="22">
<img src="https://img.shields.io/badge/CAN-3d444d?style=flat-square" alt="CAN" height="22">
<img src="https://img.shields.io/badge/RS485-3d444d?style=flat-square" alt="RS485" height="22">

**Languages**<br>
<img src="https://img.shields.io/badge/TypeScript-3d444d?style=flat-square&logo=typescript&logoColor=79c0ff" alt="TypeScript" height="22">
<img src="https://img.shields.io/badge/Python-3d444d?style=flat-square&logo=python&logoColor=79c0ff" alt="Python" height="22">
<img src="https://img.shields.io/badge/Go-3d444d?style=flat-square&logo=go&logoColor=79c0ff" alt="Go" height="22">
<img src="https://img.shields.io/badge/Kotlin-3d444d?style=flat-square&logo=kotlin&logoColor=79c0ff" alt="Kotlin" height="22">
<img src="https://img.shields.io/badge/Nix-3d444d?style=flat-square&logo=nixos&logoColor=79c0ff" alt="Nix" height="22">
<img src="https://img.shields.io/badge/Bash-3d444d?style=flat-square&logo=gnubash&logoColor=79c0ff" alt="Bash" height="22">
<img src="https://img.shields.io/badge/JavaScript-3d444d?style=flat-square&logo=javascript&logoColor=79c0ff" alt="JavaScript" height="22">

**Web and apps**<br>
<img src="https://img.shields.io/badge/Astro-3d444d?style=flat-square&logo=astro&logoColor=79c0ff" alt="Astro" height="22">
<img src="https://img.shields.io/badge/React-3d444d?style=flat-square&logo=react&logoColor=79c0ff" alt="React" height="22">
<img src="https://img.shields.io/badge/Hono-3d444d?style=flat-square&logo=hono&logoColor=79c0ff" alt="Hono" height="22">
<img src="https://img.shields.io/badge/Vite-3d444d?style=flat-square&logo=vite&logoColor=79c0ff" alt="Vite" height="22">
<img src="https://img.shields.io/badge/Tailwind_CSS-3d444d?style=flat-square&logo=tailwindcss&logoColor=79c0ff" alt="Tailwind CSS" height="22">
<img src="https://img.shields.io/badge/Drizzle-3d444d?style=flat-square&logo=drizzle&logoColor=79c0ff" alt="Drizzle" height="22">
<img src="https://img.shields.io/badge/Node.js-3d444d?style=flat-square&logo=nodedotjs&logoColor=79c0ff" alt="Node.js" height="22">
<img src="https://img.shields.io/badge/Bun-3d444d?style=flat-square&logo=bun&logoColor=79c0ff" alt="Bun" height="22">
<img src="https://img.shields.io/badge/pnpm-3d444d?style=flat-square&logo=pnpm&logoColor=79c0ff" alt="pnpm" height="22">
<img src="https://img.shields.io/badge/Quarkus-3d444d?style=flat-square&logo=quarkus&logoColor=79c0ff" alt="Quarkus" height="22">
<img src="https://img.shields.io/badge/PostgreSQL-3d444d?style=flat-square&logo=postgresql&logoColor=79c0ff" alt="PostgreSQL" height="22">
<img src="https://img.shields.io/badge/SQLite-3d444d?style=flat-square&logo=sqlite&logoColor=79c0ff" alt="SQLite" height="22">
<img src="https://img.shields.io/badge/Playwright-3d444d?style=flat-square" alt="Playwright" height="22">
<img src="https://img.shields.io/badge/Tauri-3d444d?style=flat-square&logo=tauri&logoColor=79c0ff" alt="Tauri" height="22">
<img src="https://img.shields.io/badge/Qt-3d444d?style=flat-square&logo=qt&logoColor=79c0ff" alt="Qt" height="22">
<img src="https://img.shields.io/badge/OpenCV-3d444d?style=flat-square&logo=opencv&logoColor=79c0ff" alt="OpenCV" height="22">

**AI and agents**<br>
<img src="https://img.shields.io/badge/Claude_Code-3d444d?style=flat-square&logo=claude&logoColor=79c0ff" alt="Claude Code" height="22">
<img src="https://img.shields.io/badge/Codex-3d444d?style=flat-square" alt="Codex" height="22">
<img src="https://img.shields.io/badge/Gemini-3d444d?style=flat-square&logo=googlegemini&logoColor=79c0ff" alt="Gemini" height="22">
<img src="https://img.shields.io/badge/Grok-3d444d?style=flat-square" alt="Grok" height="22">
<img src="https://img.shields.io/badge/MCP-3d444d?style=flat-square&logo=modelcontextprotocol&logoColor=79c0ff" alt="MCP" height="22">
<img src="https://img.shields.io/badge/AI_SDK-3d444d?style=flat-square&logo=vercel&logoColor=79c0ff" alt="AI SDK" height="22">
<img src="https://img.shields.io/badge/Linear-3d444d?style=flat-square&logo=linear&logoColor=79c0ff" alt="Linear" height="22">

**Infrastructure**<br>
<img src="https://img.shields.io/badge/NixOS-3d444d?style=flat-square&logo=nixos&logoColor=79c0ff" alt="NixOS" height="22">
<img src="https://img.shields.io/badge/Linux-3d444d?style=flat-square&logo=linux&logoColor=79c0ff" alt="Linux" height="22">
<img src="https://img.shields.io/badge/Cloudflare_Workers-3d444d?style=flat-square&logo=cloudflareworkers&logoColor=79c0ff" alt="Cloudflare Workers" height="22">
<img src="https://img.shields.io/badge/AWS-3d444d?style=flat-square" alt="AWS" height="22">
<img src="https://img.shields.io/badge/Docker-3d444d?style=flat-square&logo=docker&logoColor=79c0ff" alt="Docker" height="22">
<img src="https://img.shields.io/badge/Podman-3d444d?style=flat-square&logo=podman&logoColor=79c0ff" alt="Podman" height="22">
<img src="https://img.shields.io/badge/Tailscale-3d444d?style=flat-square&logo=tailscale&logoColor=79c0ff" alt="Tailscale" height="22">
<img src="https://img.shields.io/badge/GitHub_Actions-3d444d?style=flat-square&logo=githubactions&logoColor=79c0ff" alt="GitHub Actions" height="22">
<img src="https://img.shields.io/badge/GitLab_CI-3d444d?style=flat-square&logo=gitlab&logoColor=79c0ff" alt="GitLab CI" height="22">
<img src="https://img.shields.io/badge/Jenkins-3d444d?style=flat-square&logo=jenkins&logoColor=79c0ff" alt="Jenkins" height="22">
<img src="https://img.shields.io/badge/OpenTelemetry-3d444d?style=flat-square&logo=opentelemetry&logoColor=79c0ff" alt="OpenTelemetry" height="22">
<img src="https://img.shields.io/badge/SigNoz-3d444d?style=flat-square" alt="SigNoz" height="22">

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark) and (min-width: 1280px)" srcset="assets/readouts-dark.svg">
  <source media="(prefers-color-scheme: light) and (min-width: 1280px)" srcset="assets/readouts-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/readouts-dark-narrow.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/readouts-light-narrow.svg">
  <img src="assets/readouts-light.svg" alt="Seven-segment readouts: 1,019 pull requests (merged, 52 weeks), 1,250 flake commits (4 machines), 19 agent skills (in my flake), 11 upstream PRs (merged), 4 agent CLIs (one rule set).">
</picture>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark) and (min-width: 1280px)" srcset="assets/year-dark.svg">
  <source media="(prefers-color-scheme: light) and (min-width: 1280px)" srcset="assets/year-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/year-dark-narrow.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/year-light-narrow.svg">
  <img src="assets/year-light.svg" alt="Four logic analyzer channels over 52 weeks, with totals: commits 3,516, PRs opened 1,088, issues 485, private repos 12,084.">
</picture>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark) and (min-width: 1280px)" srcset="assets/bus-dark.svg">
  <source media="(prefers-color-scheme: light) and (min-width: 1280px)" srcset="assets/bus-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/bus-dark-narrow.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/bus-light-narrow.svg">
  <img src="assets/bus-light.svg" alt="A timeline drawn as a decoded bus: 2011 Code-In, started coding at 14; 2015 Dokuz Eylül, electrical and electronics; 2021 RION, electrical engineer; 2022 Kyra Tech, embedded software; 2023 ScenTronix, embedded software; 2025 NineTech, founded a consultancy; now firmware, safety-critical and AI tooling.">
</picture>
</p>

Turkish (native) · English (C1, Academic IELTS 7.0) · French (basic)

With partners I build [Kyanite Labs](https://kyanitelabs.com), a software studio, and [Status Lantern](https://github.com/StatusLantern), which watches U.S. immigration court cases and emails you when one changes. I am on [LinkedIn](https://www.linkedin.com/in/omerfarukoruc/).
