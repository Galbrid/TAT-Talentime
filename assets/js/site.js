// ===== AUTHENTICATION UTILS =====
function getAuthToken() {
  return localStorage.getItem('token');
}

function getUser() {
  return JSON.parse(localStorage.getItem('user') || '{}');
}

function isLoggedIn() {
  return !!getAuthToken();
}

function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC; SameSite=Lax";
  window.location.href = '/';
}

window.getAuthToken = getAuthToken;
window.getUser = getUser;
window.isLoggedIn = isLoggedIn;
window.logout = logout;

// ===== API CALLS =====
async function apiCall(url, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };

  const token = getAuthToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    ...options,
    headers
  });

  if (response.status === 401) {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/customer/login.html';
  }

  return response;
}

// ===== COURSE INTERACTIONS =====
async function loadPublicCourses() {
  try {
    const response = await apiCall('/api/courses/public');
    const courses = await response.json();
    displayCourses(courses);
  } catch (error) {
    console.error('Error loading courses:', error);
  }
}

function displayCourses(courses) {
  const container = document.getElementById('coursesGrid');
  if (!container) return;

  container.innerHTML = courses.map(course => `
    <div class="course-card">
      <span class="course-badge">${course.category_name || 'General'}</span>
      <h3>${course.name}</h3>
      <p class="course-description">${course.description || ''}</p>
      
      <div class="course-meta">
        <div class="meta-item">
          <span class="meta-label">⏱️ Duration:</span>
          <span class="meta-value">${course.duration || 'N/A'}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">📋 Level:</span>
          <span class="meta-value">${course.level || 'Beginner'}</span>
        </div>
      </div>

      <div class="course-highlights">
        <div class="highlights-title">Key Highlights:</div>
        <ul class="highlights-list">
          ${(course.highlights || []).slice(0, 3).map(h => `<li>${h}</li>`).join('')}
        </ul>
      </div>

      <div class="course-actions">
        <button class="btn-apply" onclick="viewCourseDetails('${course.id || course._id}')">Apply Now</button>
        <button class="btn-learn-more" onclick="viewCourseDetails('${course.id || course._id}')">Learn More</button>
      </div>
    </div>
  `).join('');
}

function viewCourseDetails(courseId) {
  const detailPath = `/course/detail.html?courseId=${encodeURIComponent(courseId)}`;
  if (isLoggedIn()) {
    window.location.href = detailPath;
  } else {
    window.location.href = `/customer/login.html?redirect=${encodeURIComponent(detailPath)}`;
  }
}

// ===== FORM SUBMISSIONS =====
document.addEventListener('DOMContentLoaded', () => {
  setupContactForm();
  setupCourseFilter();
});

function setupContactForm() {
  const form = document.querySelector('#contact-form');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const data = {
      name: form.name?.value.trim(),
      email: form.email?.value.trim(),
      phone: form.phone?.value.trim(),
      subject: form.subject?.value.trim() || 'General Inquiry',
      message: form.message?.value.trim()
    };

    try {
      const response = await fetch('/api/inquiries', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      if (response.ok) {
        form.reset();
        showMessage('Message sent successfully! We\'ll get back to you soon.', 'success');
      } else {
        showMessage(result.message || 'Failed to send message', 'error');
      }
    } catch (error) {
      showMessage('Error sending message. Please try again.', 'error');
    }
  });
}

function setupCourseFilter() {
  const filterBtns = document.querySelectorAll('[data-filter]');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const category = btn.dataset.filter;
      filterCourses(category);
    });
  });
}

function filterCourses(category) {
  const cards = document.querySelectorAll('.course-card');
  cards.forEach(card => {
    const badge = card.querySelector('.course-badge');
    if (category === 'all' || (badge && badge.textContent.trim().toLowerCase() === category.toLowerCase())) {
      card.style.display = '';
    } else {
      card.style.display = 'none';
    }
  });
}

function showMessage(message, type) {
  const div = document.createElement('div');
  div.className = `${type}-message`;
  div.textContent = message;
  div.style.cssText = `
    padding: 16px;
    margin: 16px 0;
    border-radius: 12px;
    text-align: center;
    animation: slideIn 0.3s ease;
    ${type === 'success' ? 
      'background: rgba(34, 197, 94, 0.1); color: #22c55e;' : 
      'background: rgba(220, 38, 38, 0.1); color: #dc2626;'
    }
  `;
  
  const form = document.querySelector('form');
  if (form) {
    form.insertAdjacentElement('afterend', div);
    setTimeout(() => div.remove(), 5000);
  }
}

// ===== ENROLLMENT & APPLICATIONS =====
async function applyCourse(courseId) {
  if (!isLoggedIn()) {
    window.location.href = `/customer/login.html?redirect=/course/${courseId}`;
    return;
  }

  try {
    const response = await apiCall('/api/student/apply', {
      method: 'POST',
      body: JSON.stringify({ courseId })
    });

    const result = await response.json();
    if (response.ok) {
      showMessage('Enrollment submitted! Checking your courses...', 'success');
      setTimeout(() => window.location.href = '/my-courses.html', 2000);
    } else {
      showMessage(result.message || 'Failed to apply', 'error');
    }
  } catch (error) {
    showMessage('Error submitting application', 'error');
  }
}

// ===== SMOOTH SCROLLING =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// ===== ANIMATIONS =====
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.course-card, .info-card, .testimonial-card').forEach(el => {
  observer.observe(el);
});

// ===== PAGE INITIALIZATION =====
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    initPage();
  });
} else {
  initPage();
}

async function initPage() {
  // Load categories if homepage container exists
  if (document.querySelector('.courses-filter')) {
    await loadHomepageCategories();
  }

  // Load courses if on homepage (specifically inside the courses section)
  if (document.querySelector('.courses-section #coursesGrid')) {
    loadPublicCourses();
  }

  // Update header if logged in
  setupUserMenu();
}

async function loadHomepageCategories() {
  const filterContainer = document.querySelector('.courses-filter');
  if (!filterContainer) return;

  try {
    const response = await apiCall('/api/courses/categories/');
    if (!response.ok) return;
    const categories = await response.json();
    
    // Clear and build buttons
    let html = `<button class="filter-btn active" data-filter="all">All Tracks</button>`;
    categories.forEach(cat => {
      html += `<button class="filter-btn" data-filter="${cat.name}">${cat.name}</button>`;
    });
    
    filterContainer.innerHTML = html;
    
    // Bind click events on the newly generated buttons
    setupCourseFilter();
  } catch (error) {
    console.error('Error loading homepage categories:', error);
  }
}

function setupUserMenu() {
  const user = getUser();
  const loginBtn = document.getElementById('loginBtn');
  const userMenu = document.getElementById('userMenu');
  const profileBtn = document.getElementById('profileBtn');
  const userName = document.getElementById('userName');
  const dropdownMenu = document.getElementById('dropdownMenu');

  // Inject animation and hover gap bridge styles dynamically
  if (!document.getElementById('dropdown-menu-style')) {
    const style = document.createElement('style');
    style.id = 'dropdown-menu-style';
    style.textContent = `
      #dropdownMenu {
        opacity: 0 !important;
        visibility: hidden !important;
        transform: translateY(8px) !important;
        transition: opacity 0.25s cubic-bezier(0.16, 1, 0.3, 1), transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.25s !important;
        display: block !important;
      }
      #dropdownMenu.show {
        opacity: 1 !important;
        visibility: visible !important;
        transform: translateY(0) !important;
      }
      #dropdownMenu::before {
        content: '';
        position: absolute;
        top: -12px;
        left: 0;
        right: 0;
        height: 12px;
        background: transparent;
      }
    `;
    document.head.appendChild(style);
  }

  if (isLoggedIn()) {
    if (loginBtn) loginBtn.style.display = 'none';
    if (userMenu) {
      userMenu.style.display = 'inline-block';
      
      // Update name text
      if (userName) {
        const fullName = `${user.first_name || ''} ${user.last_name || ''}`.trim() || user.email || 'Profile';
        userName.textContent = fullName;
      }
      
      // Setup dropdown toggle logic (hover and click)
      if (profileBtn && dropdownMenu) {
        let hoverTimeout;
        
        userMenu.addEventListener('mouseenter', () => {
          clearTimeout(hoverTimeout);
          dropdownMenu.classList.add('show');
        });
        
        userMenu.addEventListener('mouseleave', () => {
          hoverTimeout = setTimeout(() => {
            dropdownMenu.classList.remove('show');
          }, 150);
        });
        
        profileBtn.onclick = (e) => {
          e.stopPropagation();
          dropdownMenu.classList.toggle('show');
        };
        
        document.addEventListener('click', () => {
          dropdownMenu.classList.remove('show');
        });
      }
    }
  } else {
    if (loginBtn) loginBtn.style.display = 'inline-block';
    if (userMenu) userMenu.style.display = 'none';
  }
}

window.setupUserMenu = setupUserMenu;

document.addEventListener('DOMContentLoaded', () => {
  const bookingForm = document.querySelector('#booking-check-form');
  const bookingStatus = document.querySelector('#booking-status');
  const bookingResults = document.querySelector('#booking-results');

  if (bookingForm && bookingStatus && bookingResults) {
    bookingForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const bookingId = bookingForm.bookingId ? bookingForm.bookingId.value.trim() : '';
      const phone = bookingForm.bookingPhone ? bookingForm.bookingPhone.value.trim() : '';
      const name = bookingForm.bookingName ? bookingForm.bookingName.value.trim() : '';

      if (!bookingId && !phone && !name) {
        bookingStatus.textContent = 'Please enter booking ID, phone or name.';
        bookingStatus.style.color = '#C6922E'; // Gold for warnings/errors to adhere to strict colors
        return;
      }

      const params = new URLSearchParams();
      if (bookingId) params.append('bookingId', bookingId);
      if (phone) params.append('phone', phone);
      if (name) params.append('name', name);

      try {
        const response = await fetch(`/api/bookings/check?${params.toString()}`);
        const result = await response.json();
        if (!result.success) {
          bookingStatus.textContent = result.message || 'Unable to lookup booking.';
          bookingStatus.style.color = '#C6922E';
          return;
        }

        bookingStatus.textContent = `${result.count} booking(s) found.`;
        bookingStatus.style.color = '#007A78'; // Teal for success

        if (result.bookings.length > 0) {
          bookingResults.innerHTML = result.bookings.map((booking) => {
            const vessels = booking.vessels.map(v => `
              <li>${v.name} × ${v.quantity} (${v.unit})</li>
            `).join('');
            return `
              <div class="booking-card" style="border: 1px solid rgba(0,122,120,0.15); background: rgba(255,255,255,0.6); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px; margin-top: 15px;">
                <h4 style="color: #021B4D; margin: 0 0 10px 0;">Booking #${booking.id} — ${booking.name}</h4>
                <p style="margin: 5px 0;"><strong>Status:</strong> ${booking.status}</p>
                <p style="margin: 5px 0;"><strong>Event Date:</strong> ${booking.eventDate}</p>
                <p style="margin: 5px 0;"><strong>Phone:</strong> ${booking.phone}</p>
                <p style="margin: 5px 0;"><strong>Total:</strong> ₹${booking.totalAmount.toFixed(2)}</p>
                <p style="margin: 5px 0;"><strong>Vessels:</strong></p>
                <ul style="margin: 5px 0; padding-left: 20px;">${vessels}</ul>
              </div>
            `;
          }).join('');
        } else {
          bookingResults.innerHTML = '<p class="booking-empty" style="color: #021B4D;">No matching booking found. Please verify your details.</p>';
        }
      } catch (err) {
        bookingStatus.textContent = 'Unable to check booking right now.';
        bookingStatus.style.color = '#C6922E';
      }
    });
  }
});

