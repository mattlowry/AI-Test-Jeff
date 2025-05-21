document.addEventListener('DOMContentLoaded', function() {
    // Original script.js code and functionality remains intact
    // This file extends the functionality with mega menu additions
    
    // Add dropdown toggle indicators to dropdowns
    document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
        const indicator = document.createElement('span');
        indicator.classList.add('dropdown-indicator');
        indicator.textContent = '▼';
        toggle.appendChild(indicator);
    });

    // Ensure that dropdown menus don't disappear immediately when mouse leaves nav item
    document.querySelectorAll('.nav-links > li').forEach(item => {
        if (item.querySelector('.dropdown-menu')) {
            // Create small delay before hiding dropdown
            let timeout;
            
            item.addEventListener('mouseenter', () => {
                clearTimeout(timeout);
                document.querySelectorAll('.nav-links > li').forEach(otherItem => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('dropdown-active');
                    }
                });
                item.classList.add('dropdown-active');
            });
            
            item.addEventListener('mouseleave', () => {
                timeout = setTimeout(() => {
                    item.classList.remove('dropdown-active');
                }, 300); // 300ms delay
            });
            
            // If mouse re-enters the dropdown menu, cancel the timeout
            const dropdownMenu = item.querySelector('.dropdown-menu');
            dropdownMenu.addEventListener('mouseenter', () => {
                clearTimeout(timeout);
            });
            
            dropdownMenu.addEventListener('mouseleave', () => {
                timeout = setTimeout(() => {
                    item.classList.remove('dropdown-active');
                }, 300);
            });
        }
    });
    
    // Add keyboard navigation
    document.addEventListener('keydown', (e) => {
        // Get all visible dropdown toggles
        const visibleToggles = Array.from(document.querySelectorAll('.dropdown-toggle')).filter(toggle => {
            return window.getComputedStyle(toggle).display !== 'none';
        });
        
        // Focus a toggle or dropdown item with Tab key
        if (e.key === 'Tab') {
            const activeDropdown = document.querySelector('.nav-links > li.dropdown-active');
            if (activeDropdown) {
                const dropdownMenu = activeDropdown.querySelector('.dropdown-menu');
                if (dropdownMenu && !dropdownMenu.contains(document.activeElement)) {
                    // If we're tabbing out of the dropdown, close it
                    activeDropdown.classList.remove('dropdown-active');
                }
            }
            return; // Let default Tab behavior proceed
        }
        
        // Open dropdown with Escape key
        if (e.key === 'Escape') {
            document.querySelectorAll('.nav-links > li.dropdown-active').forEach(item => {
                item.classList.remove('dropdown-active');
            });
            return;
        }
        
        // Navigate between dropdowns with arrow keys
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
            const activeElement = document.activeElement;
            const activeDropdown = document.querySelector('.nav-links > li.dropdown-active');
            
            if (activeDropdown) {
                // Inside a dropdown
                const items = Array.from(activeDropdown.querySelectorAll('.dropdown-menu a'));
                let index = items.indexOf(activeElement);
                
                if (e.key === 'ArrowDown') {
                    index = index < items.length - 1 ? index + 1 : 0;
                } else {
                    index = index > 0 ? index - 1 : items.length - 1;
                }
                
                items[index].focus();
                e.preventDefault();
            } else if (e.key === 'ArrowDown' && activeElement.classList.contains('dropdown-toggle')) {
                // Open dropdown and focus first item
                const parentLi = activeElement.closest('li');
                parentLi.classList.add('dropdown-active');
                const firstItem = parentLi.querySelector('.dropdown-menu a');
                if (firstItem) {
                    firstItem.focus();
                    e.preventDefault();
                }
            }
        }
    });

    // Track focus for accessibility
    document.addEventListener('focusin', (e) => {
        const target = e.target;
        
        // If focus moves to a dropdown item, ensure its parent dropdown is active
        if (target.closest('.dropdown-menu')) {
            const parentLi = target.closest('.nav-links > li');
            if (parentLi) {
                document.querySelectorAll('.nav-links > li').forEach(item => {
                    if (item !== parentLi) {
                        item.classList.remove('dropdown-active');
                    }
                });
                parentLi.classList.add('dropdown-active');
            }
        }
    });
});