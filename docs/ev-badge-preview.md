---
title: "Event Badge Preview"
icon: lucide/flask-conical
---

# Event Badge Preview

This page is only for visual comparison of the currently unused `ev-badge*` styles.

## Standalone Badges

<p>
  <span class="ev-badge ev-badge-upcoming">upcoming</span>
  <span class="ev-badge ev-badge-ongoing">ongoing</span>
  <span class="ev-badge ev-badge-past">past</span>
  <span class="ev-badge ev-badge-cancelled">cancelled</span>
</p>

## On A Card

<div class="ev-card-grid">
<div class="ev-card">
  <div class="ev-card-date">4-8 May 2026</div>
  <h3 class="ev-card-title"><a href="#">Programming Formalisms</a></h3>
  <p class="ev-card-desc">Example event card with a status badge added for visual comparison.</p>
  <div class="ev-card-meta">
    <span class="ev-badge ev-badge-upcoming">upcoming</span>
    <span class="ev-format">online</span>
    <span class="diff-badge diff-intermediate">intermediate</span>
    <span class="ev-tag">Software Development</span>
    <span class="ev-tag">Testing</span>
  </div>
</div>
</div>

## Compare Variants

<div class="ev-card-grid">
<div class="ev-card">
  <div class="ev-card-date">4-8 May 2026</div>
  <h3 class="ev-card-title"><a href="#">Upcoming Variant</a></h3>
  <p class="ev-card-desc">How the badge looks in the metadata row for an upcoming event.</p>
  <div class="ev-card-meta">
    <span class="ev-badge ev-badge-upcoming">upcoming</span>
    <span class="ev-format">online</span>
    <span class="diff-badge diff-intermediate">intermediate</span>
  </div>
</div>
<div class="ev-card">
  <div class="ev-card-date">22 April 2026</div>
  <h3 class="ev-card-title"><a href="#">Ongoing Variant</a></h3>
  <p class="ev-card-desc">How the badge looks for a currently running course.</p>
  <div class="ev-card-meta">
    <span class="ev-badge ev-badge-ongoing">ongoing</span>
    <span class="ev-format">hybrid</span>
    <span class="diff-badge diff-beginner">beginner</span>
  </div>
</div>
<div class="ev-card">
  <div class="ev-card-date">15 March 2026</div>
  <h3 class="ev-card-title"><a href="#">Past Variant</a></h3>
  <p class="ev-card-desc">How the badge looks when an event has already finished.</p>
  <div class="ev-card-meta">
    <span class="ev-badge ev-badge-past">past</span>
    <span class="ev-format">online</span>
    <span class="diff-badge diff-advanced">advanced</span>
  </div>
</div>
<div class="ev-card">
  <div class="ev-card-date">TBD</div>
  <h3 class="ev-card-title"><a href="#">Cancelled Variant</a></h3>
  <p class="ev-card-desc">How the badge looks if you ever want to represent cancellations explicitly.</p>
  <div class="ev-card-meta">
    <span class="ev-badge ev-badge-cancelled">cancelled</span>
    <span class="ev-format">online</span>
    <span class="diff-badge diff-beginner">beginner</span>
  </div>
</div>
</div>
