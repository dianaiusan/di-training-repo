---
title: "Tags (Dynamic Single-Select)"
icon: lucide/tag
---

# Tags (Dynamic Single-Select)

Explore training tags. Select a tag to see courses.

## Tag Categories

- **Programming Languages**: Programming languages used across the training catalogue.
- **HPC Core**: Core HPC usage topics including systems, schedulers, modules, and environments.
- **Parallel & Performance**: Parallel programming models, accelerators, profiling, and performance work.
- **Data & AI**: Data analysis, machine learning, deep learning, and notebook-based workflows.
- **Software Engineering**: Programming, software structure, testing, and code quality.
- **Data Management & Security**: File movement, storage, sensitive data, and secure data handling environments.
- **Numerical Methods & Visualization**: Linear algebra, numerical computing, and scientific visualization methods.
- **Tools & Platforms**: Named tools, libraries, and software platforms used in the courses.

<style>
  .tag-list { display: flex; flex-wrap: wrap; gap: 0.5em; margin-bottom: 1.5em; }
  .tag-btn { padding: 0.4em 1em; border: 1px solid #aaa; border-radius: 1em; background: #f8f8f8; cursor: pointer; transition: background 0.2s, color 0.2s; }
  .tag-btn.selected { background: #0077cc; color: #fff; border-color: #0077cc; }
  .course-list { list-style: none; padding: 0; }
  .course-list li { margin-bottom: 0.5em; }
</style>
<div id="tags2-app">
  <div class="tag-list" id="tagList"></div>
  <div id="selectedTagInfo"></div>
  <ul class="course-list" id="courseList"></ul>
</div>
<script src="../../assets/javascripts/tags2.js"></script>