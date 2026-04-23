// tags2.js: Dynamic tags page logic

async function fetchTagsData() {
  const resp = await fetch('../tags/tags-courses.json');
  if (!resp.ok) throw new Error('Failed to load tags data');
  return resp.json();
}

function renderTags(tags, selectedTag) {
  const tagList = document.getElementById('tagList');
  tagList.innerHTML = '';
  Object.keys(tags).sort().forEach(tag => {
    const btn = document.createElement('button');
    btn.className = 'tag-btn' + (tag === selectedTag ? ' selected' : '');
    btn.textContent = tag;
    btn.onclick = () => selectTag(tag, tags);
    tagList.appendChild(btn);
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

function selectTag(tag, tags) {
  renderTags(tags, tag);
  renderSelectedTagInfo(tag);
  renderCourses(tags[tag]);
}

// Initial load
fetchTagsData().then(tags => {
  renderTags(tags, null);
  renderSelectedTagInfo(null);
  renderCourses([]);
});
