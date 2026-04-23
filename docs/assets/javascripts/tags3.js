// tags3.js: Multi-select dynamic tags page logic

async function fetchTagsData() {
  const resp = await fetch('../tags/tags-courses.json');
  if (!resp.ok) throw new Error('Failed to load tags data');
  return resp.json();
}

function renderTags(tags, selectedTags) {
  const tagList = document.getElementById('tagList');
  tagList.innerHTML = '';
  Object.keys(tags).sort().forEach(tag => {
    const btn = document.createElement('button');
    btn.className = 'tag-btn' + (selectedTags.includes(tag) ? ' selected' : '');
    btn.textContent = tag;
    btn.onclick = () => toggleTag(tag, tags, selectedTags);
    tagList.appendChild(btn);
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

function toggleTag(tag, tags, selectedTags) {
  const idx = selectedTags.indexOf(tag);
  if (idx === -1) {
    selectedTags.push(tag);
  } else {
    selectedTags.splice(idx, 1);
  }
  renderTags(tags, selectedTags);
  renderSelectedTagInfo(selectedTags);
  renderCourses(tags, selectedTags);
}

// Initial load
fetchTagsData().then(tags => {
  const selectedTags = [];
  renderTags(tags, selectedTags);
  renderSelectedTagInfo(selectedTags);
  renderCourses(tags, selectedTags);
});
