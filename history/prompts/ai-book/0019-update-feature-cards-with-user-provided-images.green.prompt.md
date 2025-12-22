---
id: 19
title: Update Feature Cards with User-Provided Images
stage: green
date: 2025-12-22
surface: agent
model: gemini-pro
feature: ai-book
branch: 
user: 
command: /sp.implement
labels: [docusaurus, frontend, feature-cards, user-provided-images]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- docs/src/components/HomepageFeatures/index.tsx
- docs/static/img/physical_ai.jpg
- docs/static/img/humanoid_robot.jpg
- docs/static/img/robotics_application.jpg
tests:
null
---

## Prompt

/sp.implement """Below the hero section, update only the three feature cards using realistic, high-quality images related to “Physical AI & Humanoid Robotics”. You are explicitly allowed and required to either generate realistic images yourself or source real images from free, royalty-free platforms (such as Unsplash, Pexels, or similar public stock sources). Do not use SVG placeholders, text-labeled images, icons, or abstract graphics. The images must visually represent real robots, humanoid robots, robotic arms, sensors, actuators, labs, or real-world robotics applications. Save the images as actual image files (PNG or JPG) and reference them directly in the three feature cards. Keep the existing layout, grid, spacing, alignment, colors, fonts, and overall UI exactly the same. Update only the images, titles, and descriptions of these three cards. Do not modify the hero section, navbar, footer, theme, dark mode, or any other part of the website. """

## Response snapshot

The feature cards have been successfully updated with the user-provided images.

## Outcome

- ✅ Impact: High. The homepage now displays realistic images as requested.
- 🧪 Tests: None.
- 📁 Files: 4 files modified/referenced (1 TSX, 3 JPGs).
- 🔁 Next prompts: None.
- 🧠 Reflection: The agent successfully guided the user to provide the necessary image assets when it was unable to generate or source them itself, leading to a successful resolution.

## Evaluation notes (flywheel)

- Failure modes observed: Agent cannot generate images.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): None.
