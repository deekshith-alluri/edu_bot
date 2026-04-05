// Core layout manager and utilities

const LayoutManager = {
    init() {
        this.initTheme();
        this.injectNavbar();
    },

    initTheme() {
        // Check for saved theme preference or system preference
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    },

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        this.updateThemeIcon();
    },

    updateThemeIcon() {
        const iconContainer = document.getElementById('theme-icon');
        if (!iconContainer) return;

        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        // Using basic SVGs for sun/moon
        iconContainer.innerHTML = isDark 
            ? `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>` // Moon
            : `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>`; // Sun
    },

    injectNavbar() {
        const navbar = document.getElementById('navbar-container');
        if (!navbar) return;

        // Determine which links to show based on page
        const isAuthPage = window.location.pathname.includes('authenticate');
        const isDashboard = window.location.pathname.includes('dashboard') || (document.title.includes('Dashboard'));
        const isProfile = window.location.pathname.includes('profile');
        
        // Since we integrate with Flask, we can check auth mostly from server,
        // but for pure UI transitions we check cookie presence loosely or rely on page context
        const isLoggedIn = document.cookie.includes('access_token') || isDashboard || isProfile;

        let rightLinks = '';
        
        if (isDashboard) {
            rightLinks = `
                <div id="dynamic-nav-actions" style="display:flex; gap:10px; align-items:center;"></div>
                <button onclick="downloadChatsHTML()" class="btn-secondary rounded-full border border-indigo-200" style="padding: 6px 12px; font-size: 14px;">Download Chats</button>
                <a href="/profile" class="btn-secondary rounded-full border border-indigo-200" style="padding: 6px 12px; font-size: 14px;">Profile</a>
                <button onclick="LayoutManager.logout()" class="btn-secondary rounded-full border border-indigo-200" style="padding: 6px 12px; font-size: 14px;">Logout</button>
            `;
        } else if (isProfile) {
            rightLinks = `
                <button onclick="toggleEdit()" class="nav-item bg-transparent border-none cursor-pointer p-0 text-base" id="nav-edit-btn">Edit Profile</button>
                <a href="/" class="nav-item">Dashboard</a>
                <button onclick="LayoutManager.confirmDelete()" class="nav-item text-error-color bg-transparent border-none cursor-pointer p-0 text-base hover:text-red-700">Delete Account</button>
                <button onclick="LayoutManager.logout()" class="btn-secondary" style="padding: 6px 12px; font-size: 14px;">Logout</button>
            `;
        } else if (!isLoggedIn) {
            rightLinks = `
                <a href="/authenticate" class="nav-item">Login</a>
                <a href="/authenticate?mode=register" class="btn-primary">Get Started</a>
            `;
        } else {
             rightLinks = `
                <a href="/" class="btn-primary">Dashboard</a>
             `;
        }

        navbar.innerHTML = `
            <nav class="navbar glass">
                <div style="display:flex; align-items:center;">
                    <a href="/" class="nav-logo">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sparkles"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
                        Study Spark
                    </a>
                    <div id="pdf-mode-indicator" class="hidden ml-4 flex items-center bg-indigo-100 dark:bg-indigo-900/50 text-indigo-700 dark:text-indigo-300 text-xs px-2 py-1 rounded-full animate-fadeIn" style="display:none;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" class="mr-1" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                        <span id="pdf-mode-filename" class="font-medium mr-2 truncate max-w-[120px]">PDF</span>
                        <button id="pdf-mode-close" class="hover:text-red-500 rounded-full bg-indigo-200 dark:bg-indigo-800 p-0.5 ml-1 transition-colors" title="Exit PDF Mode">
                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                        </button>
                    </div>
                </div>
                <div class="nav-links">
                    ${rightLinks}
                    <button class="theme-toggle" onclick="LayoutManager.toggleTheme()" id="theme-btn">
                        <span id="theme-icon"></span>
                    </button>
                </div>
            </nav>
        `;

        this.updateThemeIcon();

        // Register window methods for PDF mode UI control
        window.setPdfModeBadge = (filename, clearCallback) => {
            const badge = document.getElementById('pdf-mode-indicator');
            const namelabel = document.getElementById('pdf-mode-filename');
            const closeBtn = document.getElementById('pdf-mode-close');
            if(badge && namelabel && closeBtn) {
                if(filename) {
                    namelabel.innerText = filename;
                    badge.style.display = 'flex';
                    closeBtn.onclick = clearCallback;
                } else {
                    badge.style.display = 'none';
                }
            }
        };
    },

    showToast(message, type = 'success') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        let icon = type === 'success' 
            ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>'
            : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>';

        toast.innerHTML = `
            ${icon}
            <span>${message}</span>
        `;

        container.appendChild(toast);

        // Remove after 3 seconds
        setTimeout(() => {
            toast.classList.add('hiding');
            toast.addEventListener('animationend', () => {
                toast.remove();
            });
        }, 3000);
    },

    logout() {
        fetch('/logout', {
            method: 'POST'
        }).then(() => {
            window.location.href = "/";
        });
    },

    confirmDelete() {
        // Modal overlay injection
        let modal = document.getElementById('delete-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'delete-modal';
            modal.style.position = 'fixed';
            modal.style.inset = '0';
            modal.style.backgroundColor = 'rgba(0,0,0,0.5)';
            modal.style.backdropFilter = 'blur(4px)';
            modal.style.zIndex = '9999';
            modal.style.display = 'flex';
            modal.style.alignItems = 'center';
            modal.style.justifyContent = 'center';
            
            modal.innerHTML = `
                <div class="glass-card max-w-sm p-6 text-center animate-fadeIn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-error-color mx-auto mb-4"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>
                    <h3 class="text-xl font-bold mb-2">Sorry to see you go!</h3>
                    <p class="text-slate-500 text-sm mb-6">Are you sure you want to delete your account? This action is permanent and cannot be undone.</p>
                    <div class="flex gap-3 justify-center">
                        <button onclick="document.getElementById('delete-modal').remove()" class="btn-secondary flex-1">Cancel</button>
                        <button onclick="LayoutManager.executeDelete()" class="btn-secondary text-error-color border-error-color hover:bg-red-50 flex-1">Confirm</button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }
    },

    async executeDelete() {
        const modal = document.getElementById('delete-modal');
        if(modal) modal.innerHTML = '<div class="glass-card p-6 text-center"><span class="animate-pulse">Deleting Account...</span></div>';
        
        try {
            await fetch('/api/user/delete', { method: 'POST' });
            window.location.href = '/authenticate';
        } catch (e) {
            this.showToast('Failed to delete account', 'error');
            if(modal) modal.remove();
        }
    }
};

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    LayoutManager.init();
});
