// tags2.js: Dynamic tags page logic

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

function renderTags(tags, taxonomy, selectedTag) {
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
      btn.className = 'tag-btn' + (tag === selectedTag ? ' selected' : '');
      btn.textContent = tag;
      btn.onclick = () => selectTag(tag, tags, taxonomy);
      buttons.appendChild(btn);
    });

    section.appendChild(buttons);
    tagList.appendChild(section);
  });
}

function renderCourses(courses) {
  const courseList = document.getElementById('courseList');
  courseList.innerHTML = '';
  if (!courses || courses.length === 0) {
    courseList.innerHTML = '<li>No courses for this tag.</li>';
    return;
  }
  courses.forEach(course => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = course.link;
    a.textContent = course.title;
    li.appendChild(a);
    courseList.appendChild(li);
  });
}

function renderSelectedTagInfo(tag) {
  const info = document.getElementById('selectedTagInfo');
  if (tag) {
    info.innerHTML = `<strong>Selected tag:</strong> ${tag}`;
  } else {
    info.innerHTML = 'Select a tag to see courses.';
  }
}

function selectTag(tag, tags, taxonomy) {
  renderTags(tags, taxonomy, tag);
  renderSelectedTagInfo(tag);
  renderCourses(tags[tag]);
}

// Initial load
fetchTagsData().then(({ tags, taxonomy }) => {
  renderTags(tags, taxonomy, null);
  renderSelectedTagInfo(null);
  renderCourses([]);
});
