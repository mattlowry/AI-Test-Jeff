document.addEventListener('DOMContentLoaded', function() {
    // Add click handler for dropdown toggles on mobile
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            // Only handle on mobile
            if (window.innerWidth <= 768) {
                e.preventDefault();
                const parent = this.parentElement;
                
                // Close other open dropdowns
                document.querySelectorAll('.nav-links > li').forEach(item => {
                    if (item !== parent && item.classList.contains('dropdown-active')) {
                        item.classList.remove('dropdown-active');
                    }
                });
                
                // Toggle this dropdown
                parent.classList.toggle('dropdown-active');
            }
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            if (!e.target.closest('.dropdown-toggle') && !e.target.closest('.dropdown-menu')) {
                document.querySelectorAll('.dropdown-active').forEach(dropdown => {
                    dropdown.classList.remove('dropdown-active');
                });
            }
        }
    });
    
    // Handle window resize to reset mobile menu state
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            document.querySelectorAll('.dropdown-active').forEach(dropdown => {
                dropdown.classList.remove('dropdown-active');
            });
        }
    });
});