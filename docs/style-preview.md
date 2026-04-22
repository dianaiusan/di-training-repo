---
title: "Style Preview"
icon: lucide/palette
## Question: [Re]build docs/style-preview.md so it previews the current reusable component classes in docs/assets/stylesheets/extra.css, grouped by component section.
---

# Style Preview

This page previews the main reusable class groups from `docs/assets/stylesheets/extra.css`.

## Event And Self-Study Cards

### Event Card

<div class="ev-card-grid">
<div class="ev-card">
  <div class="ev-card-date">4-8 May 2026</div>
  <h3 class="ev-card-title"><a href="#">Programming Formalisms</a></h3>
  <p class="ev-card-desc">Example event card showing title, description, metadata, and tags.</p>
  <div class="ev-card-meta">
    <span class="ev-badge ev-badge-upcoming">upcoming</span>
    <span class="ev-format">online</span>
    <span class="diff-badge diff-intermediate">intermediate</span>
    <span class="ev-tag">Software Development</span>
    <span class="ev-tag">Testing</span>
  </div>
</div>
</div>

### Self-Study Card

<div class="ss-card-grid">
<div class="ss-card">
  <h3 class="ss-card-title"><a href="#">Basic Singularity/Apptainer</a></h3>
  <p class="ss-card-desc">Self-study card using the `ss-*` class family with the shared event-card visual treatment.</p>
  <div class="ss-card-meta">
    <span class="ev-format">self-study</span>
    <span class="diff-badge diff-beginner">beginner</span>
    <span class="ev-tag">Containers</span>
    <span class="ev-tag">Reproducibility</span>
  </div>
</div>
</div>

## Event Badges

<p>
  <span class="ev-badge ev-badge-upcoming">upcoming</span>
  <span class="ev-badge ev-badge-ongoing">ongoing</span>
  <span class="ev-badge ev-badge-past">past</span>
  <span class="ev-badge ev-badge-cancelled">cancelled</span>
</p>

<p>
  <span class="ev-format">online</span>
  <span class="ev-format">hybrid</span>
  <span class="ev-tag">HPC</span>
  <span class="ev-tag ev-tag-event">Event</span>
  <span class="ev-tag ev-tag-self-study">Self-study</span>
</p>

## Difficulty Badges

<p>
  <span class="diff-badge diff-beginner">beginner</span>
  <span class="diff-badge diff-intermediate">intermediate</span>
  <span class="diff-badge diff-advanced">advanced</span>
</p>

## Event Landing Cards

<div class="ev-landing-grid">
  <a class="ev-landing-card" href="#">
    <span class="ev-landing-icon">
      <img class="ev-landing-icon-img" src="/di-training-repo/assets/images/icons/calendar-days.svg" alt="">
    </span>
    <h2>Upcoming</h2>
    <p>Browse active and upcoming training sessions.</p>
  </a>
  <a class="ev-landing-card" href="#">
    <span class="ev-landing-icon">
      <img class="ev-landing-icon-img" src="/di-training-repo/assets/images/icons/book-copy.svg" alt="">
    </span>
    <h2>Past Events</h2>
    <p>Look through recently completed training.</p>
  </a>
</div>

## Bundle Track Items

<div class="bd-track">
  <div class="bd-item">
    <div class="bd-item-head">
      <div class="bd-num">1</div>
      <div class="bd-main">
        <p class="bd-title"><a href="#">Intro To HPC</a></p>
        <p class="bd-meta">1 day • beginner</p>
        <p class="bd-desc">A compact example of the bundle track item layout.</p>
        <span class="bd-badge bd-badge-core">Core</span>
        <span class="bd-badge bd-badge-hpc-infrastructure">HPC & Infrastructure</span>
        <span class="bd-badge bd-badge-foundations-levels">Foundations & Levels</span>
      </div>
    </div>
  </div>
  <div class="bd-item">
    <div class="bd-item-head">
      <div class="bd-num">2</div>
      <div class="bd-main">
        <p class="bd-title"><a href="#">Parallel Python</a></p>
        <p class="bd-meta">2 days • intermediate</p>
        <p class="bd-desc">Second track item to show spacing, numbering, and badge combinations.</p>
        <span class="bd-badge bd-badge-parallel-performance">Parallel & Performance</span>
        <span class="bd-badge bd-badge-software-development">Software Development</span>
      </div>
    </div>
  </div>
</div>

## Bundle Overview Cards

<div class="bd-card-grid">
  <a class="bd-card-link" href="#">
    <div class="bd-card">
      <h3>Intro to HPC Week</h3>
      <p>Overview-style bundle card.</p>
    </div>
  </a>
  <a class="bd-card-link" href="#">
    <div class="bd-card">
      <h3>Developer Bootcamp Week</h3>
      <p>Uses the shared overview-card hover treatment.</p>
    </div>
  </a>
</div>

## Learning Path Cards

<div class="lp-card-grid">
  <a class="lp-card-link" href="#">
    <div class="lp-card">
      <div class="lp-card-icon">
        <img class="lp-card-icon-img" src="/di-training-repo/assets/images/icons/route.svg" alt="">
      </div>
      <h3 class="lp-card-title">Beginner</h3>
      <p class="lp-card-desc">Overview card used on the learning-path landing page.</p>
    </div>
  </a>
  <a class="lp-card-link" href="#">
    <div class="lp-card">
      <div class="lp-card-icon">
        <img class="lp-card-icon-img" src="/di-training-repo/assets/images/icons/code-2.svg" alt="">
      </div>
      <h3 class="lp-card-title">Developer</h3>
      <p class="lp-card-desc">Second example to compare icon and spacing.</p>
    </div>
  </a>
</div>

## Learning Path Swimlane

<div class="lp-swimlane">
  <div class="lp-phase">
    <div class="lp-phase-header">Phase 1</div>
    <div class="lp-phase-body">
      <div class="lp-course-item"><span class="lp-course-num">1</span><span><a href="#">Linux Basics</a></span></div>
      <div class="lp-course-item"><span class="lp-course-num">2</span><span><a href="#">File Transfer</a></span></div>
    </div>
  </div>
  <div class="lp-phase-arrow">↓</div>
  <div class="lp-phase">
    <div class="lp-phase-header">Phase 2</div>
    <div class="lp-phase-body">
      <div class="lp-course-item"><span class="lp-course-num">3</span><span><a href="#">Slurm</a></span></div>
      <div class="lp-course-item"><span class="lp-course-num">4</span><span><a href="#">MPI Intro</a></span></div>
    </div>
  </div>
</div>

## Related Learning Paths

<div class="lp-related-grid">
  <div class="lp-related-card">
    <div class="lp-related-head">
      <span class="lp-related-icon">→</span>
      <p class="lp-related-title"><a href="#">Developer</a></p>
    </div>
    <p class="lp-related-desc">Compact related-card style used on detail pages.</p>
  </div>
  <div class="lp-related-card">
    <div class="lp-related-head">
      <span class="lp-related-icon">→</span>
      <p class="lp-related-title"><a href="#">Data Science</a></p>
    </div>
    <p class="lp-related-desc">Second related-card example for hover comparison.</p>
  </div>
</div>

## Tag Category Cards

<div class="tg-card-grid">
  <a class="tg-card-link" href="#">
    <div class="tg-card">
      <div class="tg-card-icon">
        <img class="tg-card-icon-img" src="/di-training-repo/assets/images/icons/tag.svg" alt="">
      </div>
      <h3 class="tg-card-title">HPC & Infrastructure</h3>
      <p class="tg-card-desc">Category overview card style.</p>
      <p class="tg-card-meta">12 courses</p>
    </div>
  </a>
  <a class="tg-card-link" href="#">
    <div class="tg-card">
      <div class="tg-card-icon">
        <img class="tg-card-icon-img" src="/di-training-repo/assets/images/icons/brain.svg" alt="">
      </div>
      <h3 class="tg-card-title">Data & AI</h3>
      <p class="tg-card-desc">Uses the same centered-card pattern.</p>
      <p class="tg-card-meta">8 courses</p>
    </div>
  </a>
</div>

## Home Card Variant

<a class="home-card-link" href="#">
  <div class="tg-card">
    <div class="tg-card-icon">
      <img class="home-card-icon-svg" src="/di-training-repo/assets/images/icons/notebook-pen.svg" alt="">
    </div>
    <h3 class="tg-card-title">Self-Study</h3>
    <p class="tg-card-desc">Home-page variant built on top of the tag-card pattern.</p>
  </div>
</a>

## Tag Detail Cards

<div class="tag-grid">
  <div class="tag-card">
    <p class="tag-card-name">Python</p>
    <ul class="tag-card-courses">
      <li><a class="tag-course-link" href="#">Intro to Python for HPC</a></li>
      <li><a class="tag-course-link" href="#">Parallel Python</a></li>
    </ul>
  </div>
  <div class="tag-card">
    <p class="tag-card-name">Containers</p>
    <ul class="tag-card-courses">
      <li><a class="tag-course-link" href="#">Basic Singularity/Apptainer</a></li>
      <li><a class="tag-course-link" href="#">Container Workflows</a></li>
    </ul>
  </div>
</div>

<p><a class="tag-page-link" href="#">Example tag page link</a></p>

## Scientific Domain Cards

<div class="sd-card-grid">
  <a class="sd-card-link" href="#">
    <div class="sd-card">
      <div class="sd-card-icon">
        <img class="sd-card-icon-img" src="/di-training-repo/assets/images/icons/flask-conical.svg" alt="">
      </div>
      <h3 class="sd-card-title">Computational Science</h3>
      <p class="sd-card-meta">6 courses</p>
    </div>
  </a>
  <a class="sd-card-link" href="#">
    <div class="sd-card">
      <div class="sd-card-icon">
        <img class="sd-card-icon-img" src="/di-training-repo/assets/images/icons/dna.svg" alt="">
      </div>
      <h3 class="sd-card-title">Bioinformatics</h3>
      <p class="sd-card-meta">4 courses</p>
    </div>
  </a>
</div>

## Per-Course Tag Row

<div class="tag-list">
  <span class="ev-tag">Python</span>
  <span class="ev-tag">HPC</span>
  <span class="ev-tag">Jupyter</span>
</div>
