// Theme Toggling
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');
    
    if (body.classList.contains('light-mode')) {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        themeIcon.setAttribute('data-lucide', 'sun');
    } else {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        themeIcon.setAttribute('data-lucide', 'moon');
    }
    lucide.createIcons();
    localStorage.setItem('theme', body.classList.contains('dark-mode') ? 'dark' : 'light');
}

// Persist Theme
if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.remove('light-mode');
    document.body.classList.add('dark-mode');
    setTimeout(() => {
        document.getElementById('theme-icon')?.setAttribute('data-lucide', 'sun');
        lucide.createIcons();
    }, 100);
}

// Smooth Scroll
function scrollToSection(id) {
    document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
}

// Advisor Form Submission
const advisorForm = document.getElementById('advisor-form');
const resultsPlaceholder = document.getElementById('results-placeholder');
const loadingSpinner = document.getElementById('loading');
const productList = document.getElementById('product-list');

advisorForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // UI State: Loading
    resultsPlaceholder.classList.add('hidden');
    productList.innerHTML = '';
    loadingSpinner.classList.remove('hidden');

    const formData = new FormData(advisorForm);
    const data = {
        category: formData.get('category'),
        budget: formData.get('budget'),
        preferences: formData.get('preferences')
    };

    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error('API Error');

        const products = await response.json();
        renderProducts(products);
    } catch (err) {
        console.error(err);
        resultsPlaceholder.innerHTML = `<p style="color:red">Failed to fetch recommendations. Is the server running?</p>`;
        resultsPlaceholder.classList.remove('hidden');
    } finally {
        loadingSpinner.classList.add('hidden');
    }
});

function renderProducts(products) {
    if (products.length === 0) {
        resultsPlaceholder.innerHTML = `<p>No products found within this budget. Try increasing it!</p>`;
        resultsPlaceholder.classList.remove('hidden');
        return;
    }

    productList.innerHTML = products.map((p, idx) => `
        <div class="product-card" style="animation-delay: ${idx * 0.1}s">
            <div class="rating">⭐ ${p.rating}</div>
            <h4>${p.name}</h4>
            <p class="product-price">₹${p.price.toLocaleString()}</p>
            <div class="features">
                ${p.features.map(f => `<span class="feature-tag">${f}</span>`).join('')}
            </div>
            <button class="btn primary-btn" style="margin-top:auto; padding: 0.6rem">View Details</button>
        </div>
    `).join('');
}

// Scroll Animations
const observerOptions = {
    threshold: 0.2
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-visible');
        }
    });
}, observerOptions);

document.querySelectorAll('.content-section, .card').forEach(el => {
    el.classList.add('fade-in-hidden');
    observer.observe(el);
});
