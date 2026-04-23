// tags3.js: Multi-select dynamic tags page logic

async function fetchTagsData() {
  const [tagsResp, taxonomyResp] = await Promise.all([
    fetch('../tags/tags-courses.json'),
    fetch('../tags/tags-taxonomy.json').catch(() => null),
  ]);

  if (!tagsResp.ok) throw new Error('Failed to load tags data');

  let taxonomy = null;
  if (taxonomyResp && taxonomyResp.ok) {
    taxonomy = await taxonomyResp.json();
  }

  return {
    tags: await tagsResp.json(),
    taxonomy,
  };
}

function buildCategoryEntries(tags, taxonomy) {
  if (!taxonomy) {
    return [{ key: 'all', title: 'All Tags', description: '', tags: Object.keys(tags).sort() }];
  }

  const grouped = {};
  Object.keys(tags).forEach(tag => {
    const category = taxonomy.tag_to_category[tag] || 'other';
    if (!grouped[category]) grouped[category] = [];
    grouped[category].push(tag);
  });

  return taxonomy.category_order
    .filter(category => grouped[category] && grouped[category].length)
    .map(category => ({
      key: category,
      title: taxonomy.category_meta[category]?.title || category,
      description: taxonomy.category_meta[category]?.description || '',
      tags: grouped[category].sort(),
    }));
}

function renderTags(tags, taxonomy, selectedTags) {
  const tagList = document.getElementById('tagList');
  tagList.innerHTML = '';

  buildCategoryEntries(tags, taxonomy).forEach(category => {
    const section = document.createElement('div');
    section.className = 'tag-category';

    const heading = document.createElement('h3');
    heading.textContent = category.title;
    section.appendChild(heading);

    if (category.description) {
      const description = document.createElement('p');
      description.textContent = category.description;
      section.appendChild(description);
    }

    const buttons = document.createElement('div');
    buttons.className = 'tag-list';

    category.tags.forEach(tag => {
      const btn = document.createElement('button');
      btn.className = 'tag-btn' + (selectedTags.includes(tag) ? ' selected' : '');
      btn.textContent = tag;
      btn.onclick = () => toggleTag(tag, tags, taxonomy, selectedTags);
      buttons.appendChild(btn);
    });

    section.appendChild(buttons);
    tagList.appendChild(section);
  });
}

function renderCourses(tags, selectedTags) {
  const courseList = document.getElementById('courseList');
  courseList.innerHTML = '';
  if (!selectedTags.length) {
    courseList.innerHTML = '<li>Select one or more tags to see courses.</li>';
    return;
  }
  // Collect all unique courses that have any of the selected tags
  const courseMap = {};
  selectedTags.forEach(tag => {
    (tags[tag] || []).forEach(course => {
      courseMap[course.slug] = course;
    });
  });
  const courses = Object.values(courseMap);
  if (!courses.length) {
    courseList.innerHTML = '<li>No courses for these tags.</li>';
    return;
  }
  courses.sort((a, b) => a.title.localeCompare(b.title));
  courses.forEach(course => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = course.link;
    a.textContent = course.title;
    li.appendChild(a);
    courseList.appendChild(li);
  });
}

function renderSelectedTagInfo(selectedTags) {
  const info = document.getElementById('selectedTagInfo');
  if (selectedTags.length) {
    info.innerHTML = `<strong>Selected tag${selectedTags.length > 1 ? 's' : ''}:</strong> ${selectedTags.join(', ')}`;
  } else {
    info.innerHTML = 'Select one or more tags to see courses.';
  }
}

function toggleTag(tag, tags, taxonomy, selectedTags) {
  const idx = selectedTags.indexOf(tag);
  if (idx === -1) {
    selectedTags.push(tag);
  } else {
    selectedTags.splice(idx, 1);
  }
  renderTags(tags, taxonomy, selectedTags);
  renderSelectedTagInfo(selectedTags);
  renderCourses(tags, selectedTags);
}

// Initial load
fetchTagsData().then(({ tags, taxonomy }) => {
  const selectedTags = [];
  renderTags(tags, taxonomy, selectedTags);
  renderSelectedTagInfo(selectedTags);
  renderCourses(tags, selectedTags);
});
