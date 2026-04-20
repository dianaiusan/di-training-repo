(() => {
  const TAG_OVERVIEW_SEGMENT = "/explore/tags/";

  function normalizeWhitespace(value) {
    return (value || "").replace(/\s+/g, " ").trim();
  }

  function getTagBadgeContainer() {
    return document.querySelector(".md-content .md-tags");
  }

  function getTagSpans(container) {
    return Array.from(container.querySelectorAll("span.md-tag"));
  }

  function getOverviewUrl() {
    const overviewLink = document.querySelector('a[href$="/explore/tags/"], a[href*="/explore/tags/"]');
    if (!overviewLink) {
      return new URL(`${TAG_OVERVIEW_SEGMENT}`, window.location.origin).toString();
    }

    const url = new URL(overviewLink.getAttribute("href"), window.location.href);
    const markerIdx = url.pathname.indexOf(TAG_OVERVIEW_SEGMENT);
    if (markerIdx < 0) {
      return new URL(`${TAG_OVERVIEW_SEGMENT}`, window.location.origin).toString();
    }

    return new URL(url.pathname.slice(0, markerIdx) + TAG_OVERVIEW_SEGMENT, url.origin).toString();
  }

  function collectCategoryUrls(overviewUrl) {
    const links = Array.from(document.querySelectorAll('a[href*="/explore/tags/"]'));
    const categoryUrls = new Set();

    links.forEach((link) => {
      const href = link.getAttribute("href");
      if (!href) {
        return;
      }

      const absolute = new URL(href, window.location.href);
      const pathname = absolute.pathname;
      if (!pathname.includes(TAG_OVERVIEW_SEGMENT)) {
        return;
      }

      if (pathname.endsWith("/explore/tags/") || pathname.endsWith("/explore/tags")) {
        return;
      }

      categoryUrls.add(absolute.toString());
    });

    if (categoryUrls.size === 0) {
      return [];
    }

    return Array.from(categoryUrls).sort();
  }

  async function fetchCategoryPages(urls) {
    const pages = [];

    for (const url of urls) {
      try {
        const response = await fetch(url, { credentials: "same-origin" });
        if (!response.ok) {
          continue;
        }
        const text = await response.text();
        pages.push({ url, text: text.toLowerCase() });
      } catch (_error) {
        // Ignore fetch failures and continue with available pages.
      }
    }

    return pages;
  }

  function escapeRegExp(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  function tagToDisplay(tag) {
    return normalizeWhitespace(tag.replace(/-/g, " "));
  }

  function findCategoryForTag(tag, categoryPages) {
    const tagText = normalizeWhitespace(tag).toLowerCase();
    const displayText = tagToDisplay(tag).toLowerCase();

    const strictTagRegex = new RegExp(
      `<h4 class="tag-card-name">\\s*${escapeRegExp(tagText)}\\s*</h4>`,
      "i"
    );

    const displayRegex = new RegExp(
      `<h4 class="tag-card-name">\\s*${escapeRegExp(displayText)}\\s*</h4>`,
      "i"
    );

    for (const page of categoryPages) {
      if (strictTagRegex.test(page.text) || displayRegex.test(page.text)) {
        return page.url;
      }
    }

    return null;
  }

  function replaceBadgesWithLinks(spans, mapping, fallbackUrl) {
    spans.forEach((span) => {
      const tag = normalizeWhitespace(span.textContent);
      if (!tag) {
        return;
      }

      const href = mapping.get(tag.toLowerCase()) || fallbackUrl;
      const link = document.createElement("a");
      link.className = span.className;
      link.href = href;
      link.textContent = tag;
      link.title = `Open tag page for ${tag}`;
      span.replaceWith(link);
    });
  }

  async function makeTagBadgesClickable() {
    const container = getTagBadgeContainer();
    if (!container) {
      return;
    }

    const spans = getTagSpans(container);
    if (spans.length === 0) {
      return;
    }

    const overviewUrl = getOverviewUrl();
    const categoryUrls = collectCategoryUrls(overviewUrl);
    const categoryPages = await fetchCategoryPages(categoryUrls);

    const mapping = new Map();
    spans.forEach((span) => {
      const tag = normalizeWhitespace(span.textContent);
      if (!tag || mapping.has(tag.toLowerCase())) {
        return;
      }
      const categoryUrl = findCategoryForTag(tag, categoryPages);
      if (categoryUrl) {
        mapping.set(tag.toLowerCase(), categoryUrl);
      }
    });

    replaceBadgesWithLinks(spans, mapping, overviewUrl);
  }

  document.addEventListener("DOMContentLoaded", () => {
    makeTagBadgesClickable();
  });
})();
